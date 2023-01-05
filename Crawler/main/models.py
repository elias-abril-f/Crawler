from django.db import models

# Create your models here.
class Property(models.Model):
    
    price = models.CharField(max_length=255, null=False)
    numberBedrooms = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, null=False)
    area = models.CharField(max_length=255, null=False)
    postcode = models.CharField(max_length=255, null=False)
    url = models.CharField(max_length=255, null=False)
    img = models.CharField(max_length=255, null=False)
    

    def __str__(self):
        return self.code