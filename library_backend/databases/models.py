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