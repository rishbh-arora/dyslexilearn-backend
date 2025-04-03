from django.urls import path, include
from api.views.views import ping, progress_data
from api.urls import learning, auth

urlpatterns = [
    path('ping/', ping),
    path('auth/', include(auth)),
    path('learning/', include(learning)),
    path('progress/', progress_data)
]
