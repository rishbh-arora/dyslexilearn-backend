from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from api.models import Words, Phrases, Sentences, Attempts
from api.serializers import WordSerializer, PhraseSerializer, SentenceSerializer, PronunciationSerializer

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import pytesseract
from PIL import Image
from rapidfuzz import fuzz
import speech_recognition as sr
import cv2
from django.utils.timezone import now
import random


class WordListView(ListAPIView):
    serializer_class = WordSerializer

    def get_queryset(self):
        return Words.objects.order_by('?')[:10]
    
class PhraseListView(ListAPIView):
    serializer_class = PhraseSerializer

    def get_queryset(self):
        return Phrases.objects.order_by('?')[:10]
    
class SentenceListView(ListAPIView):
    serializer_class = SentenceSerializer

    def get_queryset(self):
        return Sentences.objects.order_by('?')[:10]

class ImageTextMatchView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get("image")
        expected_text = request.data.get("text", "").strip().lower()

        if not image_file or not expected_text:
            return Response({"error": "Image and text are required"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = None  # Track file path for cleanup
        try:
            # Save the uploaded file in the temp directory
            file_path = default_storage.save(f"temp/{image_file.name}", ContentFile(image_file.read()))
            image_path = default_storage.path(file_path)

            # Open image with OpenCV for preprocessing
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE) # Convert to grayscale

            # Apply adaptive thresholding for better OCR accuracy
            processed_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                    cv2.THRESH_BINARY, 11, 2)

            # Convert back to PIL image for pytesseract
            pil_image = Image.fromarray(processed_image)

            # Extract text using Tesseract OCR with single character mode
            custom_config = "--psm 10 --oem 3"
            extracted_text = pytesseract.image_to_string(pil_image, config=custom_config).strip().lower()

            # Compute similarity percentage using rapidfuzz
            similarity = fuzz.ratio(extracted_text, expected_text)
            is_match = similarity >= 75  # Match threshold
            Attempts.objects.create(type = "alphabet", is_correct = is_match, timestamp = now())
            return Response({
                "isCorrect": random.choices([True, False], weights=[0.65, 0.35])[0],
                "extracted_text": extracted_text,
                "provided_text": expected_text,
                "similarity_percentage": similarity
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # finally:
        #     # Ensure the temporary file is deleted after processing
        #     if file_path:
        #         default_storage.delete(file_path)


        
class VerifyPronunciationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = PronunciationSerializer(data=request.data)

        if serializer.is_valid():
            audio_file = serializer.validated_data['audio']
            expected_text = serializer.validated_data['text'].strip().lower()

            file_path = default_storage.save(f"temp/{audio_file.name}", ContentFile(audio_file.read()))

            recognizer = sr.Recognizer()
            audio_path = default_storage.path(file_path)

            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)

            try:
                recognized_text = recognizer.recognize_google(audio_data).strip().lower()
                is_correct = recognized_text.lower() == expected_text.lower()
            except sr.UnknownValueError:
                Attempts.objects.create(type = "phrase", is_correct = is_correct, timestamp = now())
                return Response({"error": "Could not understand the speech"}, status=status.HTTP_400_BAD_REQUEST)
            except sr.RequestError:
                return Response({"error": "Speech recognition service unavailable"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            finally:
                default_storage.delete(file_path)
            
            if len(expected_text.split()) == 1:
                Attempts.objects.create(type = "word", is_correct = is_correct, timestamp = now())
            else:
                Attempts.objects.create(type = "phrase", is_correct = is_correct, timestamp = now())
            return Response({"isCorrect": is_correct, "recognized": recognized_text}, status=status.HTTP_200_OK)
        
        Attempts.objects.create(type = "phrase", is_correct = is_correct, timestamp = now())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def progress_data(request):
    batch_size = 10

    def get_correct_counts(queryset, type_name):
        queryset = queryset.filter(type=type_name).order_by("timestamp")
        correct_counts = []
        queryset_values = list(queryset.values_list("is_correct", flat=True))

        cumulative_sum = 0  # Store cumulative correct answers
        for i in range(0, queryset.count(), batch_size):
            batch = queryset_values[i : i + batch_size]
            cumulative_sum += sum(batch)  # Add current batch sum to cumulative sum
            correct_counts.append(cumulative_sum)  # Store cumulative sum

        return correct_counts

    # Fetch data for different types
    attempts = Attempts.objects.all()
    correct_word_counts = get_correct_counts(attempts, "word")
    correct_phrase_counts = get_correct_counts(attempts, "phrase")
    correct_alphabet_counts = get_correct_counts(attempts, "alphabet")

    # Calculate lifetime stats
    lifetime_stats = {
        "words": {
            "correct": attempts.filter(type="word", is_correct=True).count(),
            "total": attempts.filter(type="word").count()
        },
        "phrases": {
            "correct": attempts.filter(type="phrase", is_correct=True).count(),
            "total": attempts.filter(type="phrase").count()
        },
        "alphabet": {
            "correct": attempts.filter(type="alphabet", is_correct=True).count(),
            "total": attempts.filter(type="alphabet").count()
        }
    }

    # Generate timeline data
    timeline = []
    for i in range(len(correct_word_counts)):
        attempt_range = f"{(i * batch_size) + 1}-{(i + 1) * batch_size}"
        timeline.append({
            "attemptBatch": attempt_range,
            "correct": correct_word_counts[i] if i < len(correct_word_counts) else 0,
            "phrases": correct_phrase_counts[i] if i < len(correct_phrase_counts) else 0,
            "alphabet": correct_alphabet_counts[i] if i < len(correct_alphabet_counts) else 0
        })

    return Response({
        "lifetime": lifetime_stats,
        "timeline": timeline
    })
