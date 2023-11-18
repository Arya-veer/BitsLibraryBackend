from django.db import models
from django.utils import timezone

from misc.models import AbstractBaseModel

def libraryOverviewImagePath(instance,filename):
    return f"Images/LibraryOverview/{filename}"

# Create your models here.
class LibraryOverview(AbstractBaseModel):

    title = models.CharField(max_length=100,blank=True,default="About BITS Pilani Library")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=libraryOverviewImagePath,null=True,blank=True)
    is_set = models.BooleanField(default=False,unique=True)

    def save(self,*args, **kwargs):
        if LibraryOverview.objects.filter(is_set = True).exists():
            if self.is_set == True:
                LibraryOverview.objects.all().update(is_set = False)
        else:
            self.is_set = True
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.title} - {self.is_set}"
    
class LibraryCollection(AbstractBaseModel):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    is_set = models.BooleanField(default=False,unique=True)

    def save(self,*args, **kwargs):
        if LibraryCollection.objects.filter(is_set = True).exists():
            if self.is_set == True:
                LibraryCollection.objects.all().update(is_set = False)
        else:
            self.is_set = True
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Library Collection"

    
class LibraryCollectionData(AbstractBaseModel):

    resource = models.CharField(max_length=100,unique=True)
    data = models.TextField(null=True,blank=True)
    is_int = models.BooleanField(default=False)
    collection = models.ForeignKey(LibraryCollection,models.CASCADE,related_name="data")

    def __str__(self) -> str:
        return f"{self.resource} - {self.data}"
    
class LibraryRulesAndRegulation(AbstractBaseModel):

    name = models.CharField(max_length=200)
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.is_set}"

class Rule(AbstractBaseModel):

    text = models.TextField(blank=True)
    is_bold = models.BooleanField(default=False)
    parent = models.ForeignKey(LibraryRulesAndRegulation,on_delete=models.CASCADE,related_name="rules")

    def __str__(self) -> str:
        return f"{self.text}"

class TabularRule(AbstractBaseModel):

    name = models.CharField(max_length=100,blank=True)
    table = models.JSONField(null=True)
    parent = models.ForeignKey(LibraryRulesAndRegulation,on_delete=models.CASCADE,related_name="tables")

    def __str__(self) -> str:
        return f"{self.name}"

class LibraryCommittee(AbstractBaseModel):
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=True,unique=True)

    def __str__(self) -> str:
        return f"{self.description}"

class LibraryCommitteeMember(AbstractBaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    department = models.CharField(max_length=200,blank=True)
    is_present = models.BooleanField(default=True)
    image = models.ImageField(upload_to='Images/LibraryCommitteeMembers',blank=True,null=True)
    committee = models.ForeignKey(LibraryCommittee,on_delete=models.CASCADE,related_name="members")

    def __str__(self) -> str:
        return f"{self.name}-{self.department}"

class LibraryTeam(AbstractBaseModel):
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.description}"

def libraryTeamMemberImagePath(instance,filename):
    return f"Images/LibraryMember/{instance.designation}/{instance.name}/{filename}"

class LibraryTeamMember(AbstractBaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=20,blank=True)
    designation = models.CharField(max_length=200,blank=True)
    is_present = models.BooleanField(default=True)
    team = models.ForeignKey(LibraryTeam,on_delete=models.CASCADE,related_name="members")
    image = models.ImageField(upload_to=libraryTeamMemberImagePath,blank=True,null=True)
    is_librarian = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name}-{self.designation}"
    

class LibraryBrochure(AbstractBaseModel):
    uploaded_on = models.DateTimeField(default=timezone.now)
    file = models.FileField(max_length=200,upload_to='brochure')
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return super().__str__()

class LibraryWebsiteUserGuide(AbstractBaseModel):
    uploaded_on = models.DateTimeField(default=timezone.now)
    file = models.FileField(max_length=200,upload_to='user_guide')
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return super().__str__()

class LibraryTiming(AbstractBaseModel):
    uploaded_on = models.DateTimeField(default=timezone.now)
    imgae = models.ImageField(max_length=200,upload_to='timings')
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return super().__str__()


class Event(AbstractBaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100,blank=True)
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.date} - {self.time}"

class News(AbstractBaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    url = models.URLField(blank=True,max_length=200)
    is_set = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.date}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class BookMarquee(AbstractBaseModel):
    isbn = models.CharField(max_length=20)
    is_set = models.BooleanField(default=True)
    uploaded_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Book Marquee"
        verbose_name_plural = "Book Marquees"
    
    def __str__(self) -> str:
        return f"{self.isbn} - {self.is_set}"