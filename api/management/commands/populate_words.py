from django.core.management.base import BaseCommand
from api.models import Words

class Command(BaseCommand):
    help = "Populate the Words table with predefined words"

    def handle(self, *args, **kwargs):
        random_words = [
            "apple", "bicycle", "river", "mountain", "galaxy",
            "ocean", "thunder", "sunrise", "whisper", "shadow",
            "lantern", "puzzle", "horizon", "melody", "crystal",
            "breeze", "echo", "compass", "wildfire", "twilight"
        ]

        # Create Word objects if they don't exist
        for word in random_words:
            Words.objects.get_or_create(word=word)

        self.stdout.write(self.style.SUCCESS("Successfully populated the Words table!"))
