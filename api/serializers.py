from rest_framework import serializers
from .models import Words, Phrases, Sentences

class WordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Words
        fields = ['word', 'random_case']

class PhraseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phrases
        fields = ['phrase', 'random_case']

class SentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sentences
        fields = ['sentence', 'random_case']

class PronunciationSerializer(serializers.Serializer):
    audio = serializers.FileField()
    text = serializers.CharField(max_length=100)