from django.urls import path
from .views import TextLLMView, SpeechLLMView, TTSView, SpeechASRView, SpeechToSpeechView

urlpatterns = [

    path('text_llm_url/', TextLLMView.as_view()),
    path('speech_llm_url/', SpeechLLMView.as_view()),
    path('speech_asr_url/', SpeechASRView.as_view()),
    path('tts_url/', TTSView.as_view()),
    path('speech_to_speech_url/', SpeechToSpeechView.as_view()),
]
