from django.core.management.base import BaseCommand
from api.models import Phrases

class Command(BaseCommand):
    help = "Populate the Phrases table with predefined data"

    def handle(self, *args, **kwargs):
        phrases = [
            "Break the ice",
            "Burn the midnight oil",
            "Bite the bullet",
            "Hit the nail on the head",
            "Let the cat out of the bag",
            "Under the weather",
            "A piece of cake",
            "Once in a blue moon",
            "Spill the beans",
            "Back to the drawing board"
        ]

        for phrase in phrases:
            Phrases.objects.get_or_create(phrase=phrase)

        self.stdout.write(self.style.SUCCESS("Successfully populated the Phrases table!"))
