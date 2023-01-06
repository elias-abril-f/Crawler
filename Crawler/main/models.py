from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Property(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.CharField(max_length=255, null=True)
    numberBedrooms = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    area = models.CharField(max_length=255, null=True)
    postcode = models.CharField(max_length=255, null=True)
    url = models.CharField(max_length=255, null=True)
    img = models.CharField(max_length=255, null=True)
    search=models.CharField(max_length=255, null=True)
    dateTime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)
    
class User(AbstractUser):
    property = models.ManyToManyField(Property, blank=True,null=True)
    def __str__(self):
        return self.username