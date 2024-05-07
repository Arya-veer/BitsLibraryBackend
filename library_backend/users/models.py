from django.db import models
from django.contrib.auth.models import User
from misc.models import AbstractBaseModel
from django.utils import timezone

STATUS_OF_CLAIM = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected')
]

# Create your models here.
class UserProfile(models.Model):

    auth_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    name = models.CharField("Name of the person",max_length=150)
    uid = models.CharField(unique=True,max_length=20)
    phone_number = models.BigIntegerField(null=True,blank=True)
    user_type = models.CharField(max_length=20,default="Student",choices=(("Student","Student"),("Faculty","Faculty"),("Staff","Staff"),("Research Scholar","Research Scholar"),("Alumni","Alumni"),("Other","Other"),("Admin","Admin")))

    def __str__(self) -> str:
        return f"{self.name} - {self.uid}"


def item_path(instance,filename):
    return f"items/{instance.name}_{filename}"

class Item(AbstractBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    dt = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name

class Claim(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='claims')
    item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='claims')
    date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=8, choices=STATUS_OF_CLAIM, default='Pending')
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.item} - {self.date}"



class ArticleBookRequest(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='article_requests')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    extra_data = models.JSONField(default=dict)
    type_doc = models.CharField(max_length=200,default="Article",choices=(("Article","Article"),("Book","Book")))
    status = models.CharField(max_length=200,default="Pending",choices=(("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")))
    date = models.DateTimeField(auto_now_add=True)
    # remarks = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.title}"

    class Meta:
        verbose_name = "Article Request"
        verbose_name_plural = "Article Requests"


class FreeBook(AbstractBaseModel):

    fbn = models.IntegerField()
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    year = models.IntegerField()
    edition = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Free Book"
        verbose_name_plural = "Free Books"

    def __str__(self) -> str:
        return f"{self.title} - {self.author}"
    

class FreeBookPick(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='free_book_picks')
    book = models.ForeignKey(FreeBook,on_delete=models.CASCADE,related_name='free_book_picks')
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=200,default="Pending",choices=(("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")))

    class Meta:
        verbose_name = "Free Book Pick"
        verbose_name_plural = "Free Book Picks"

    def __str__(self) -> str:
        return f"{self.user} - {self.book} - {self.date}"

class FootageRequest(models.Model):
    
    student = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='footage_requests')
    request = models.TextField()
    status = models.CharField(max_length=200,default="Pending",choices=(("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected"),("Closed","Closed")))
    remarks = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "CCTV Footage Request"
        verbose_name_plural = "CCTV Footage Requests"
    
    def __str__(self) -> str:
        return f"{self.student} - {self.start_time} - {self.end_time}"
    