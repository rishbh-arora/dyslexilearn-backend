import random

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Words(models.Model):
    word = models.CharField(max_length=200)

    @property
    def random_case(self):
        return ''.join(random.choice([c.lower(), c.upper()]) for c in self.word)

class Phrases(models.Model):
    phrase = models.CharField(max_length=200)

    @property
    def random_case(self):
        return ''.join(random.choice([c.lower(), c.upper()]) for c in self.phrase)
    
class Sentences(models.Model):
    sentence = models.CharField(max_length=1000)

    @property
    def random_case(self):
        return ''.join(random.choice([c.lower(), c.upper()]) for c in self.sentence)
    
class Attempts(models.Model):
    TYPE_CHOICES = [
        ("word", "Word"),
        ("phrase", "Phrase"),
        ("alphabet", "Alphabet"),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField()