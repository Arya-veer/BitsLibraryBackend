from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Campus,Database,ELearning,NewArrival,Platform

@receiver(post_delete,sender=Campus)
def delete_campus_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete,sender=Database)
def delete_database_image(sender,instance,**kwargs):
    if instance.user_guide_file:
        instance.user_guide_file.delete(False)

@receiver(post_delete,sender=ELearning)
def delete_elearning_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete,sender=NewArrival)
def delete_new_arrival_image(sender,instance,**kwargs):
    if instance.file:
        instance.file.delete(False)

@receiver(post_delete,sender=Platform)
def delete_platform_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)