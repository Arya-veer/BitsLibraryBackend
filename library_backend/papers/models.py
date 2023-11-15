from django.db import models
from misc.models import AbstractBaseModel
# Create your models here.

class BITSCampus(AbstractBaseModel):
    name = models.CharField(max_length=60,primary_key=True)

    class Meta:
        verbose_name = "BITS Campus"
        verbose_name_plural = "BITS Campuses"
    
    def __str__(self) -> str:
        return self.name

class Course(AbstractBaseModel):
    name = models.CharField(max_length=60,blank=True)
    course_id = models.CharField(max_length=60,blank=True)
    # campus = models.ForeignKey(BITSCampus,on_delete=models.CASCADE,related_name='courses',default='Pilani')

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return f"{self.name} ({self.course_id})"

def paper_path(instance, filename):
    return f'papers/{instance.course.course_id}/{instance.year}/{instance.semester}/{filename}'



class Paper(AbstractBaseModel):
    semester = models.CharField(max_length=60,blank=True,choices=[('First','First'),('Second','Second')])
    year = models.IntegerField(blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='papers',null = True)
    file = models.FileField(upload_to=paper_path,blank=True,null=True)
    hide = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Paper"
        verbose_name_plural = "Papers"
    
    def __str__(self):
        return f"{self.course.course_id} {self.semester} {self.year}"


class TextBook(AbstractBaseModel):
    title = models.CharField(max_length=200,blank=True)
    extra_data = models.JSONField(default=dict,blank=True,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='textbooks',null = True)
    url = models.URLField(max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = "TextBook"
        verbose_name_plural = "TextBooks"
    
    def __str__(self):
        return f"{self.title} ({self.course.course_id})"