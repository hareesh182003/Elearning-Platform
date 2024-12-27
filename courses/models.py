from django.db import models
from django.contrib.auth.models import User
from django.core import validators
# Create your models here.
class Course(models.Model):
    course_title = models.CharField(max_length=100)
    course_subtitle = models.CharField(max_length=100)
    course_description = models.TextField()
    course_bullets = models.TextField()

    def __str__(self):
        return self.course_title
    
class Profile(models.Model):
    username = models.OneToOneField(User,on_delete= models.CASCADE) 
    address = models.TextField()
    profile_pic = models.ImageField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return str(self.username)
    
