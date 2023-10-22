from django.db import models

# Create your models here.

class LinkClass(models.Model):

    name = models.CharField("Heading",primary_key=True,max_length=100)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Link Class"
        verbose_name_plural = "Link Classes"
     
    def __str__(self) -> str:
        return self.name
    
def image_path_link_site(obj,filename):
    return f"{obj.link_class}/{obj.site_name}_{filename}"


class LinkSite(models.Model):

    site_name = models.CharField("Name of the site",primary_key=True,max_length=100)
    image = models.ImageField(max_length=200,upload_to=image_path_link_site)
    link_class = models.ForeignKey(LinkClass,models.CASCADE,related_name='sites')
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "Link Site"
        verbose_name_plural = "Link Sites"

    def __str__(self) -> str:
        return f"{self.site_name} - {self.link_class}"

    
class OpenETDs(models.Model):
    
        name = models.CharField("Name of the site",primary_key=True,max_length=100)
        url = models.URLField(max_length=200)
    
        class Meta:
            verbose_name = "OpenETDs"
            verbose_name_plural = "OpenETDs"
    
        def __str__(self) -> str:
            return self.name
