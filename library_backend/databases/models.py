from django.db import models

from misc.models import AbstractBaseModel

# Create your models here.
class Campus(AbstractBaseModel):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    is_main = models.BooleanField(default=False)
    image = models.ImageField(upload_to='campus_images',blank=True,null=True)
    extra_data = models.JSONField(default=dict,blank=True,null=True)
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name

class Database(AbstractBaseModel):
    name = models.CharField(max_length=60,blank=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,related_name='databases',null = True)
    link = models.URLField(max_length=200,null=True,blank=True)
    description = models.TextField(blank=True)
    is_trial = models.BooleanField(default=False)
    user_guide_file = models.FileField(upload_to='database_user_guides',blank=True,null=True)
    user_guide_url = models.URLField(max_length=200,null=True,blank=True)

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"

    def __str__(self):
        return self.name
    


class Publisher(AbstractBaseModel):
    name = models.TextField(blank=True)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
    
    def __str__(self):  
        return self.name

class Subject(AbstractBaseModel):
    name = models.TextField(blank=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
    
    def __str__(self):  
        return self.name


    
class EBook(AbstractBaseModel):
    name = models.TextField(blank=True)
    author = models.TextField(blank=True)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,related_name='books',null = True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='books',null = True)
    url = models.URLField(max_length=200,null=True,blank=True)
    extra_data = models.JSONField(default=dict,blank=True,null=True)
    
    class Meta:
        verbose_name = "E-Book"
        verbose_name_plural = "E-Books"

    def __str__(self):
        return f"{self.name} - {self.author}"


class EJournal(AbstractBaseModel):
    name = models.TextField(blank=True)
    publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE,related_name='journals',null = True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='journals',null = True)
    url = models.URLField(max_length=200,null=True,blank=True)
    extra_data = models.JSONField(default=dict,blank=True,null=True)
    
    class Meta:
        verbose_name = "E-Journal"
        verbose_name_plural = "E-Journals"

    def __str__(self):
        return f"{self.name}"
    

class ELearning(AbstractBaseModel):

    site_name = models.CharField(max_length=60)
    url = models.URLField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='elearning_images',blank=True,null=True)

    class Meta:
        verbose_name = "E-Learning"
        verbose_name_plural = "E-Learnings"
    
    def __str__(self):
        return self.site_name

class OpenAccess(AbstractBaseModel):
    
    name = models.CharField(max_length=60)
    link = models.URLField(max_length=200,null=True,blank=True)

    class Meta:
        verbose_name = "Open Access"
        verbose_name_plural = "Open Access"
    
    def __str__(self):
        return self.name
    

def new_arrival_path(instance, filename):
    return f'new_arrivals/{instance.year}/{instance.month}/{filename}'

class NewArrival(AbstractBaseModel):

    month = models.CharField(max_length=20)
    year = models.IntegerField()
    file = models.FileField(upload_to=new_arrival_path,blank=True,null=True)

    class Meta:
        verbose_name = "New Arrival"
        verbose_name_plural = "New Arrivals"
    
    def __str__(self):
        return f"{self.month} {self.year}"
        

class Platform(AbstractBaseModel):

    name = models.CharField(max_length=60)
    link = models.URLField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='platform_images',blank=True,null=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,related_name='platforms',null = True)

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"
    
    def __str__(self):
        return self.name


