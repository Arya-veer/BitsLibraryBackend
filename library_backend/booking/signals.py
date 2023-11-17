from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Room


@receiver(post_delete,sender=Room)
def delete_room_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)