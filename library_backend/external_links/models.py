from django.db import models

# Create your models here.

    
def image_path_link_site(obj,filename):
    return f"Sites/{obj.site_name}_{filename}"


class LinkSite(models.Model):

    site_name = models.CharField("Name of the site",primary_key=True,max_length=100)
    image = models.ImageField(max_length=200,upload_to=image_path_link_site)
    link_type = models.CharField(max_length=100,choices=[("Research Assistance","Research Assistance"),("Open ETDs","Open ETDs")],default="Research Assistance")
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "Link Site"
        verbose_name_plural = "Link Sites"

    def __str__(self) -> str:
        return f"{self.site_name} - {self.link_type}"

    
class InflibnetLink(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "INFLIBNET Link"
        verbose_name_plural = "INFLIBNET Links"

    def __str__(self) -> str:
        return f"{self.name} - {self.url}"