from rest_framework import views,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# from library_backend.settings import CHATBOT
from chatbot.chatbot import ChatBot

# Create your views here.


class AskQuestionAPI(views.APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        question = request.data.get("question")
        if not question:
            return Response({"answer":"Hey! How can I help you?"},status = status.HTTP_400_BAD_REQUEST)
        chatbot = ChatBot.get_object()
        if chatbot is None:
            return Response({"answer":"Chatbot is not initialized."},status = status.HTTP_400_BAD_REQUEST)
        try:
            answer = chatbot.respond(question)
            return Response({"answer":answer},status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"answer":"Some error has occured"},status = status.HTTP_400_BAD_REQUEST)
        