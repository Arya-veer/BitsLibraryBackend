import os

from rest_framework import views,generics,status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils.Scripts.scripts_handler import ScriptsHandler

from users.permissions import AdminPermission

from .serializers import *

from library_backend.settings import MEDIA_URL
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
    
    def create_path(self,file):
        return "https://library.bits-pilani.ac.in/back/" + os.path.join(MEDIA_URL,"Templates",file)
    
    
    def get(self,request):
        return Response({"types":data_excel_types,"links":[{"name":template,"link":self.create_path(TEMPLATES[template])} for template in TEMPLATES]},status=status.HTTP_200_OK)
    

class DataExcelUploadAPI(generics.CreateAPIView):
    serializer_class = DataExcelUploadSerializer
    permission_classes = (AdminPermission,)
    
    def create(self, request, *args, **kwargs):
        try:    
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data_excel_obj = serializer.save()
            handler = ScriptsHandler(data_excel=data_excel_obj)
            handler.populate()
            return Response({"message":"Excel uploaded successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            data_excel_obj.errors.add(str(e))
            data_excel_obj.status = "Failed"
            data_excel_obj.save()
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        

class DataExcelListAPI(generics.ListAPIView):
    serializer_class = DataExcelListSerializer
    permission_classes = (AdminPermission,)
    queryset = DataExcel.objects.all().order_by('-created_at')
