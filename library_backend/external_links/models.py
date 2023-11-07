from django.db import models
from misc.models import AbstractBaseModel
# Create your models here.

    
def image_path_link_site(obj,filename):
    s = f"Sites/{obj.site_name}_{filename}"
    return s


class LinkSite(AbstractBaseModel):

    site_name = models.CharField("Name of the site",primary_key=True,max_length=100)
    image = models.ImageField(max_length=200,upload_to=image_path_link_site)
    link_type = models.CharField(max_length=100,choices=[("Research Assistance","Research Assistance"),("Open ETDs","Open ETDs"),("Download Form","Download Form"),("Inflibnet","Inflibnet")],default="Research Assistance")
    url = models.URLField(max_length=200,null=True,blank=True)
    file = models.FileField(upload_to='link_sites/',null=True,blank=True)
    site_type = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name = "Link Site"
        verbose_name_plural = "Link Sites"

    def __str__(self) -> str:
        return f"{self.site_name} - {self.link_type}"

    
class InflibnetLink(AbstractBaseModel):

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "INFLIBNET Link"
        verbose_name_plural = "INFLIBNET Links"

    def __str__(self) -> str:
        return f"{self.name} - {self.url}"