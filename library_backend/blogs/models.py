from django.db import models

from misc.models import AbstractBaseModel


# Create your models here.
class Blog(AbstractBaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images',blank=True,null=True)
    published_date = models.DateField(null=True,blank=True)
    archived = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
    
    def __str__(self) -> str:
        return self.title