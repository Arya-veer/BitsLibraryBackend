from typing import Any
from django.db import models
from django.utils import timezone
import uuid
import requests
import json
from library_backend.settings import FRONTEND_BASE_URL
from library_backend.keyconfig import FRONTEND_API_KEY


# Create your models here.

URL_MAP = {
    "FreqAskedQuestion":["/misc/faq",],
    "Feedback":["/misc/feedback",],
    "Course":["/services/pyq/[campus]","/services/pyq/[campus]/[course]","/services/textbooks","/services/textbooks/[course]"],
    "Paper":["/services/pyq/[campus]/[course]",],
    "TextBook":["/services/textbooks/[course]",],
    "LibraryCollection":["/","/about/library_collection", "/othercampus/[campus]", "/othercampus"],
    "LibraryCollectionData":["/","/about/library_collection", "/othercampus/[campus]", "/othercampus"],
    "LibraryRulesAndRegulation":["/about/rules",],
    "Rule":["/about/rules",],
    "TabularRule":["/about/rules",],
    "LibraryCommittee":["/about/committee/committee",],
    "LibraryCommitteeMember":["/about/committee/committee",],
    "LibraryTeam":["/about/committee/team",],
    "LibraryTeamMember":["/about/committee/team",],
    "LibraryBrochure":["/about/brochure",],
    "LibraryWebsiteUserGuide":["/links/[type]",],
    "LibraryCalendar":["/about/timings",],
    "Event":["/news/events","/"],
    "News":["/news/news","/"],
    "Campus":["/databases/[campus]","/links/[type]"],
    "Database":["/databases/[campus]",],
    "EBook":["/eresources/ebooks",],
    "Publisher":["/eresources/ebooks","/eresources/ejournals",],
    "Subject":["/eresources/ebooks","/eresources/ejournals",],
    "EJournal":["/eresources/ejournals",],
    "ELearning":["/links/[type]",],
    "Platform":["/eresources/ebooks","/links/[type]"],
    "OpenAccess":["/links/[type]",],
    "LinkSite":["/links/[type]",],
    "NewArrival":["/links/[type]",],
    "BookMarquee":["/","/about/library_collection", "/othercampus/[campus]"],
    "DonatedBook":["/services/donated_books",],
    "GalleryImage":["/about/gallery",],
    "NewArrival":["/links/[type]",],
    "FreeBook":["/me/pick_book",],
    "Item":["/me/lost_and_found",],
    "Inflibnet":["/links/[type]",],
    "Blog":["/newsletters", "/newsletters/[id]"],
}

class AbstractBaseModel(models.Model):

    to_revalidate = True
    class Meta:
        abstract = True
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.front_url = URL_MAP.get(self.__class__.__name__,[])

    def validate(self):
        if self.to_revalidate:
            for url in self.front_url:
                Revalidate.add(url)


    def delete(self, using = "default", keep_parents = False) :
        super().delete(using, keep_parents)
        self.validate()
    
    def save(self, *args, **kwargs ) -> None:
        super().save(*args, **kwargs)
        self.validate()


class HomePage(AbstractBaseModel):

    heading = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100)
    description = models.TextField()
    is_set = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


class FreqAskedQuestion(AbstractBaseModel):

    question = models.CharField(max_length=200)
    answer = models.TextField()
    is_set = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Frequently Asked Question"
        verbose_name_plural = "Frequently Asked Questions"
    
    def __str__(self):
        return self.question
    
        

class Feedback(AbstractBaseModel):

    name = models.CharField(max_length=100)
    feedback = models.TextField()
    designation = models.CharField(max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='feedbacks/',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
    
    def __str__(self) -> str:
        return f"{self.name}"
    

class LibraryDocument(AbstractBaseModel):

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='library_documents/')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Library Document"
        verbose_name_plural = "Library Documents"

    
    def __str__(self) -> str:
        return self.name
    

class Revalidate(models.Model):

    url = models.CharField(max_length=200,unique=True)
    timestamp = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)
    res = models.JSONField(null=True)

    class Meta:
        verbose_name = "Revalidate"
        verbose_name_plural = "Revalidate"

    @classmethod
    def add(cls,url):
        if url[0] != "/":
            url = "/" + url
        obj,created = cls.objects.get_or_create(url=url)
        if not created:
            obj.save()

    def revalidate(self):
        data = {
            "url":self.url,
            "api_key":FRONTEND_API_KEY
        }
        try:
            response = requests.post(FRONTEND_BASE_URL+"/user/revalidate",json=data)
            self.res = json.loads(response.content)
            if response.status_code == 200:
                self.done = True
            else:
                self.done = False
        except Exception as e:
            # print(e)
            self.done = False
        
        self.timestamp = timezone.now()
    
    def __str__(self) -> str:
        return self.url + " " + str(self.timestamp)
    
    
    def save(self, *args, **kwargs) -> None:
        
        self.revalidate()
        super().save(*args, **kwargs)
    


class WebsiteText(models.Model):
    static_id = models.UUIDField(unique=True,default=uuid.uuid4)
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    revalidate_url = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Website Text"
        verbose_name_plural = "Website Texts"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        Revalidate.add(self.revalidate_url)


TEMPLATES = {
    "EBooks":"ebooks.xlsx",
    "EJournals":"ejournals.xlsx",
    "Faculty":"faculty.xlsx",
    "Student":"student.xlsx"
}

status_types = [
    "Pending",
    "Completed",
    "Failed"
]
data_excel_types = list(TEMPLATES.keys())
DATA_EXCEL_CHOICES = list(zip(data_excel_types,data_excel_types))
STATUS_CHOICES = list(zip(status_types,status_types))
class DataExcel(models.Model):
    excel = models.FileField(upload_to="data_excel/")
    created_at = models.DateTimeField(auto_now=True)
    errors = models.JSONField(default=list)
    purpose = models.CharField(max_length=100,null=True,blank=True,choices=DATA_EXCEL_CHOICES)
    status = models.CharField(max_length=100, default="Pending", null=True, blank=True, choices=STATUS_CHOICES)
    
    class Meta:
        verbose_name = "Data Excel"
        verbose_name_plural = "Data Excels"
    
    def __str__(self) -> str:
        return f"{self.purpose} - {self.created_at}" 