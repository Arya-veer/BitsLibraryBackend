from django.db import models

# Create your models here.
class Campus(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    is_main = models.BooleanField(default=False)
    image = models.ImageField(upload_to='campus_images',blank=True,null=True)
    extra_data = models.JSONField(default=dict,blank=True,null=True)
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name

class Database(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,related_name='databases',null = True)
    link = models.URLField(max_length=200,null=True,blank=True)
    description = models.TextField(blank=True)
    is_trial = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"

    def __str__(self):
        return self.name
    


class Publisher(models.Model):
    name = models.TextField(blank=True)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
    
    def __str__(self):  
        return self.name

class Subject(models.Model):
    name = models.TextField(blank=True)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
    
    def __str__(self):  
        return self.name


    
class EBook(models.Model):
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


class EJournal(models.Model):
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
    

class ELearning(models.Model):

    site_name = models.CharField(max_length=60)
    url = models.URLField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='elearning_images',blank=True,null=True)

    class Meta:
        verbose_name = "E-Learning"
        verbose_name_plural = "E-Learnings"
    
    def __str__(self):
        return self.site_name

class OpenAccess(models.Model):
    
    name = models.CharField(max_length=60)
    link = models.URLField(max_length=200,null=True,blank=True)

    class Meta:
        verbose_name = "Open Access"
        verbose_name_plural = "Open Access"
    
    def __str__(self):
        return self.name
        

class Platform(models.Model):

    name = models.CharField(max_length=60)
    link = models.URLField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='platform_images',blank=True,null=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,related_name='platforms',null = True)

    class Meta:
        verbose_name = "Platform"
        verbose_name_plural = "Platforms"
    
    def __str__(self):
        return self.name
