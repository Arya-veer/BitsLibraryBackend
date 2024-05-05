from .models import Feedback,LibraryDocument,DataExcel
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete,sender=Feedback)
def delete_feedback_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete,sender=LibraryDocument)
def delete_feedback_file(sender,instance,**kwargs):
    if instance.file:
        instance.file.delete(False)
        
@receiver(post_delete,sender=DataExcel)
def delete_excel_file(sender,instance,**kwargs):
    if instance.excel:
        instance.excel.delete(False)