from django.shortcuts import render

from rest_framework import generics,views,status
# Create your views here.

from .models import Course, Paper

from .serializers import CourseSerializer, PaperSerializer

class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search',None)
        if search is not None:
            qs = qs.filter(name__icontains=search) | qs.filter(course_id__icontains=search)
        return qs.distinct('course_id')

class PaperList(generics.ListAPIView):
    serializer_class = PaperSerializer

    def get_queryset(self):
        qs = Paper.objects.all()
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