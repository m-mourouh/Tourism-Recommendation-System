from datetime import datetime
from django.db import models
from django.contrib.auth.hashers import make_password , check_password
from django.db.models.fields import CharField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls.resolvers import URLPattern
from django.utils import timezone
import os
import random

def filepath(request,filename):
    old_filename = filename
    timeNow = datetime.now().strftime('%Y%m%d%H:%M:%S') + str(random.sample(range(0, 1000), 10))
    filename = "%s%s" % (timeNow,old_filename)
    return os.path.join('upload/',filename)

class Client(models.Model): 
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100 ,unique=True)
    birthdate = models.DateField()
    address = models.CharField(max_length=255,null=True, blank=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    gender = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    h_version = models.IntegerField()
    profile_img = models.ImageField(upload_to=filepath,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # return f'{self.firstname} {self.lastname}'
        return f'{self.firstname} {self.lastname}'

    # hashage de mot passe
    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super(Client, self).save(*args, **kwargs)

class Hotel(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    review = models.IntegerField()
    score = models.FloatField()
    price = models.FloatField()
    country = models.CharField(default='Maroc',max_length=100)
    city = models.CharField(default='Marrakech',max_length=100)
    location = models.CharField(max_length=250)
    image = models.CharField(max_length=550)
    amenities = models.CharField(max_length=350)

    def __str__(self):          
        return f'{self.name}' 

class Rating(models.Model):
    client  = models.ForeignKey(Client,on_delete=models.CASCADE) 
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])
    comment = models.TextField(default='')
    datePosted = models.DateTimeField(default=timezone.now,blank=True)
    def __str__(self):          
        return f'{self.client.firstname} {self.client.lastname} | {self.rating} | {self.hotel.name}'




