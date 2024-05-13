from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ContextFile

@receiver(post_delete,sender=ContextFile)
def delete_context_file(sender,instance,**kwargs):
    if instance.file:
        instance.file.delete()
