from django.db import models

# Create your models here.
class Campus(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    is_main = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return self.name

class Database(models.Model):
    name = models.CharField(max_length=60,blank=True,primary_key=True)
    campus = models.ForeignKey(Campus,on_delete=models.CASCADE,related_name='databases')
    link = models.URLField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Database"
        verbose_name_plural = "Databases"

    def __str__(self):
        return self.name