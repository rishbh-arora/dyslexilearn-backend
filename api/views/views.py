from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .auth import google_auth_callback
from .learning import (
    WordListView,
    SentenceListView,
    PhraseListView,
    VerifyPronunciationView,
    ImageTextMatchView,
    progress_data
)

@api_view(["GET"])
def ping(request: Request) -> Response:
    return Response({"status": "ok", "message": "pong"}, status.HTTP_200_OK)