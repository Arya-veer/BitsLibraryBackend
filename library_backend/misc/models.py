from django.db import models
from django.utils import timezone

# Create your models here.

class HomePage(models.Model):

    heading = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100)
    description = models.TextField()
    is_set = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class NewArrivals(models.Model):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    is_set = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class FreqAskedQuestion(models.Model):

    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_set = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"
    
    def __str__(self):
        return self.question

class Feedback(models.Model):

    name = models.CharField(max_length=100)
    feedback = models.TextField()
    designation = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='feedbacks/',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
    
    def __str__(self) -> str:
        return f"{self.name}"
