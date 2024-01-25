from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_delete,sender=LinkSite)
def delete_link_site_image(sender,instance,**kwargs):
    if instance.file:
        instance.file.delete(False)

