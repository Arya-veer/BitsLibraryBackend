
from .views import *
from django.urls import path
urlpatterns = [
    path('ask_question/', AskQuestionAPI.as_view()),
    path('retrain/', ChatBotRetrainAPI.as_view())
]
