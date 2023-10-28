from rest_framework import views,generics
from rest_framework.permissions import AllowAny

from .serializers import *
# Create your views here.
class HomePageAPI(generics.RetrieveAPIView):
    serializer_class = HomePageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        try:
            return HomePage.objects.get(is_set = True)
        except:
            return HomePage.objects.filter(is_set=True).order_by('-uploaded_on').first()
        
class FreqAskedQuestionsListAPI(generics.ListAPIView):
    serializer_class = FreqAskedQuestionSerializer
    queryset = FreqAskedQuestion.objects.all().order_by('question')

class FeedbackListCreateAPI(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.filter(show = True).order_by('-created_at')