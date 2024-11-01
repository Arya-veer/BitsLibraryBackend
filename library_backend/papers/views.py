from django.shortcuts import render

from rest_framework import generics,views,status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from .models import Course, Paper,TextBook

from .serializers import CourseSerializer, PaperSerializer,TextBookSerializer

class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search',None)
        if search is not None:
            qs = qs.filter(name__icontains=search) | qs.filter(course_id__icontains=search)
        campus = self.request.query_params.get('campus','Pilani')
        qs = qs.filter(campus__name=campus)
        course_type = self.request.query_params.get('course_type',None)
        if course_type is not None and course_type == 'paper':
            qs = qs.filter(id__in = Paper.objects.filter(campus__name = campus).values_list('course',flat=True))
        elif course_type is not None and course_type == 'textbook':
            qs = qs.filter(id__in = TextBook.objects.all().values_list('course',flat=True))
        qs = qs.distinct('course_id')
        return qs.order_by('course_id')
    
class CourseDetail(views.APIView):

    def get(self,request):
        course = Course.objects.filter(course_id=self.request.query_params.get('course_id',None)).first()
        if course is None:
            return views.Response(status=status.HTTP_404_NOT_FOUND)
        return views.Response(CourseSerializer(course).data,status=status.HTTP_200_OK)

        
class PaperList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaperSerializer

    def get_queryset(self):
        qs = Paper.objects.all()
        hidden = self.request.query_params.get('hidden',None)
        if hidden is None:
            qs = qs.filter(hide=False)
        campus = self.request.query_params.get('campus',None)
        if campus is not None:
            qs = qs.filter(campus__name=campus)
        course_id = self.request.query_params.get('course_id',None)
        exam = self.request.query_params.get('exam',None)
        year = self.request.query_params.get('year',None)
        if course_id is not None:
            qs = qs.filter(course__course_id=course_id)
        if exam is not None:
            qs = qs.filter(exam=exam)
        if year is not None:
            qs = qs.filter(year=year)
        return qs

class YearListAPI(views.APIView):
    def get(self,request):
        qs = Paper.objects.all()
        course_id = self.request.query_params.get('course_id',None)
        exam = self.request.query_params.get('exam',None)
        if course_id is not None:
            qs = qs.filter(course__course_id=course_id)
        if exam is not None:
            qs = qs.filter(exam=exam)
        years = qs.values_list('year',flat=True).distinct()
        return views.Response(years,status=status.HTTP_200_OK)
    

class TextBookListAPI(generics.ListAPIView):

    serializer_class = TextBookSerializer

    def get_queryset(self):
        return TextBook.objects.filter(course__course_id = self.request.query_params.get('course_id',None))