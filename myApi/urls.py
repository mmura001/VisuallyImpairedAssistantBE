from django.urls import path
from .views import gemini_chat

urlpatterns = [
    path('gemini-chat/',gemini_chat, name='gemini_chat'),
]

