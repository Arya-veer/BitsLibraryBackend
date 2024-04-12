from rest_framework import views,generics,status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.Scripts.scripts_handler import ScriptsHandler

from users.permissions import AdminPermission

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

class WebsiteTextRetrieveAPI(generics.RetrieveAPIView):
    serializer_class = WebsiteTextSerializer
    queryset = WebsiteText.objects.all()
    lookup_field = 'static_id'
    


class DataExcelTypesListAPI(views.APIView):
    permission_classes = (AdminPermission,)
    
    def get(self,request):
        return Response({"types":list(SCRIPT_TO_CLASS_MAPPING.keys())},status=status.HTTP_200_OK)
    

class DataExcelUploadAPI(generics.CreateAPIView):
    serializer_class = DataExcelUploadSerializer
    permission_classes = (AdminPermission,)
    
    def create(self, request, *args, **kwargs):
        try:
            data_excel_obj = super().create(request, *args, **kwargs).data
            handler = ScriptsHandler(data_excel=data_excel_obj)
            handler.populate()
            return Response({"message":"Excel uploaded successfully"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)