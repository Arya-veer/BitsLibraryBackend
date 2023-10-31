from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=60,blank=True)
    course_id = models.CharField(max_length=60,blank=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return f"{self.name} ({self.course_id})"

def paper_path(instance, filename):
    return f'papers/{instance.course.course_id}/{instance.year}/{instance.semester}/{filename}'



class Paper(models.Model):
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
