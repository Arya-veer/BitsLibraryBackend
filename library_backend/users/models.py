from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):

    auth_user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    name = models.CharField("Name of the person",max_length=150)
    uid = models.CharField(unique=True,max_length=20)
    phone_number = models.BigIntegerField(null=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.uid}"