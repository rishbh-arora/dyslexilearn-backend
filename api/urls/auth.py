from django.urls import path, include
from api.views.views import google_auth_callback

urlpatterns = [
    path('login/callback/', google_auth_callback, name='google_auth_callback'),
    path('accounts/', include('allauth.urls')),
]
