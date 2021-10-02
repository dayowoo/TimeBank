from django.db import models

# Create your models here.
# Location
class Location(models.Model):
    name = models.CharField(max_length=15)
    location = models.CharField(max_length=50, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)




class Category(models.Model):
    category_name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ["category_name"]
    
    def __str__(self):
        return self.category_name
    
class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)