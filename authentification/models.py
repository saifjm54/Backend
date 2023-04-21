from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
class PatientAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    tel = models.CharField(max_length=12)
    birthday = models.DateTimeField(format('dd-mm-yyyy'))
    gender = models.CharField(max_length=10)
        
class Status(models.Model):
    status = models.CharField(max_length=100)

class Speciality(models.Model):
    speciality = models.CharField(max_length=100)

class Country(models.Model):
    country = models.CharField(max_length=100)
class Ville(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ville = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
class Adress(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    rue = models.CharField(max_length=100)
    num = models.IntegerField(null=True)

class PraticienAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=12)
    speciality = models.ManyToManyField(Speciality)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
