from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    auth_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    name = models.CharField("Name of the person",max_length=150)
    uid = models.CharField(unique=True,max_length=20)
    phone_number = models.BigIntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.uid}"


def item_path(instance,filename):
    return f"items/{instance.name}_{filename}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


    def __str__(self) -> str:
        return self.name

class Claim(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='claims')
    item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='claims')
    date = models.DateField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
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

    def __str__(self) -> str:
        return f"{self.user} - {self.title}"

    class Meta:
        verbose_name = "Article Request"
        verbose_name_plural = "Article Requests"
