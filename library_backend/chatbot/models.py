from django.db import models
from .chatbot import ChatBot,CONTEXT_FILE

# Create your models here.


class ContextFile(models.Model):
    file = models.FileField(upload_to=CONTEXT_FILE)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.file)
    
    def save(self,*args, **kwargs):
        # self.name = self.file.name
        super(ContextFile,self).save(*args, **kwargs)
        ChatBot.retrain()