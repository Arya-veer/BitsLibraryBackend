from collections.abc import Iterable
from django.db import models
from django.utils import timezone

import requests
from library_backend.settings import FRONTEND_BASE_URL
from library_backend.keyconfig import FRONTEND_API_KEY

# Create your models here.

URL_MAP = {
    "FreqAskedQuestion":"/misc/faq"
}

class AbstractBaseModel(models.Model):

    url = URL_MAP.get(__name__)
    to_revalidate = True
    class Meta:
        abstract = True

    
    def save(self, force_insert , force_update , using , update_fields ) -> None:
        super().save(force_insert, force_update, using, update_fields)
        if self.to_revalidate:
            Revalidate.add(AbstractBaseModel.url)


class HomePage(AbstractBaseModel):

    heading = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100)
    description = models.TextField()
    is_set = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class NewArrivals(AbstractBaseModel):

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    is_set = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

class FreqAskedQuestion(AbstractBaseModel):

    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_set = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"
    
    def __str__(self):
        return self.question
    
        

class Feedback(AbstractBaseModel):

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
    

class LibraryDocument(AbstractBaseModel):

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='library_documents/')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Library Document"
        verbose_name_plural = "Library Documents"

    
    def __str__(self) -> str:
        return self.name
    

class Revalidate(AbstractBaseModel):

    url = models.CharField(max_length=200,unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Revalidate"
        verbose_name_plural = "Revalidate"

    @classmethod
    def add(cls,url):
        obj,created = cls.objects.get_or_create(url=url)
        if not created:
            obj.save()

    def revalidate(self):
        data = {
            "url":self.url,
            "api_key":FRONTEND_API_KEY
        }
        response = requests.post(FRONTEND_BASE_URL+"/user/revalidate",data)
        print(response.content)
        if response.status_code == 200:
            self.done = True
        else:
            self.done = False
        self.timestamp = timezone.now()
    
    def __str__(self) -> str:
        return self.url + " " + str(self.timestamp)
    
    
    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        self.revalidate()
        super().save(force_insert, force_update, using, update_fields)
    
        