from django.core.management.base import BaseCommand
from api.models import Sentences

class Command(BaseCommand):
    help = "Populate the Sentences table with predefined data"

    def handle(self, *args, **kwargs):
        sentences = [
            "The sun sets in the west",
            "A journey of a thousand miles begins with a single step",
            "Knowledge is power",
            "Time and tide wait for no one",
            "Actions speak louder than words",
            "The early bird catches the worm",
            "Fortune favors the bold",
            "Honesty is the best policy",
            "Practice makes perfect",
            "Hard work beats talent when talent doesn't work hard"
        ]

        for sentence in sentences:
            Sentences.objects.get_or_create(sentence=sentence)

        self.stdout.write(self.style.SUCCESS("Successfully populated the Sentences table!"))
