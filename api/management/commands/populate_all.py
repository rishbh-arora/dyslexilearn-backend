from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Run all population commands (Words, Sentences, and Phrases)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting to populate all tables..."))

        try:
            call_command("populate_words")
            self.stdout.write(self.style.SUCCESS("Successfully populated the Words table!"))

            call_command("populate_sentences")
            self.stdout.write(self.style.SUCCESS("Successfully populated the Sentences table!"))

            call_command("populate_phrases")
            self.stdout.write(self.style.SUCCESS("Successfully populated the Phrases table!"))

            self.stdout.write(self.style.SUCCESS("All tables populated successfully! 🎉"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
