from rest_framework import views,status
from rest_framework.response import Response
# Create your views here.


class AskQuestionAPI(views.APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        question = request.data.get("question")
        if not question:
            return Response({"error":"Please provide a question."},status = status.HTTP_400_BAD_REQUEST)
        