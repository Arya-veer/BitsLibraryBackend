from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import *


@receiver(post_delete,sender=LibraryOverview)
def delete_library_overview_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete,sender = LibraryTeamMember)
def delete_library_team_member_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)

@receiver(post_delete,sender = LibraryCommitteeMember)
def delete_library_committee_member_image(sender,instance,**kwargs):
    if instance.image:
        instance.image.delete(False)


@receiver(post_delete,sender = LibraryBrochure)
def delete_library_brochure_file(sender,instance,**kwargs):
    if instance.file:
        instance.file.delete(False)

@receiver(post_delete,sender = LibraryTiming)
def delete_library_timing_image(sender,instance,**kwargs):
    if instance.imgae:
        instance.imgae.delete(False)