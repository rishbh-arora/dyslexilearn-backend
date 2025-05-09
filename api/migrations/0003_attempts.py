# Generated by Django 5.1.7 on 2025-03-29 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_phrases_sentences_words_delete_announcement_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('word', 'Word'), ('phrase', 'Phrase'), ('alphabet', 'Alphabet')], max_length=10)),
                ('is_correct', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]
