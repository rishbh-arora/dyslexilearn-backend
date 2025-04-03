from django.urls import path
from api.views.views import (
    WordListView,
    SentenceListView,
    PhraseListView,
    VerifyPronunciationView,
    ImageTextMatchView
)

urlpatterns = [
    path("words/", WordListView.as_view()),
    path("phrases/", PhraseListView.as_view()),
    path("sentences/", SentenceListView.as_view()),
    path("verify-pronunciation", VerifyPronunciationView.as_view()),
    path("verify-letter", ImageTextMatchView.as_view())
]
