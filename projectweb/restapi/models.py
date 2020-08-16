from django.db import models
from datetime import datetime
# Create your models here.

class Blog(models.Model):
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    body = models.TextField(default='')
    time = models.DateTimeField(default = datetime.today)
    status = models.CharField(default='0',max_length=200)

    email= models.EmailField()
    college = models.CharField(max_length = 200, default='')
    branch = models.CharField(max_length = 200, default='')
    fullname = models.CharField(max_length=200, default='')
    key = models.CharField(max_length=200)

    def __str__(self):
        return self.author


class Users(models.Model):
    email= models.EmailField()
    college = models.CharField(max_length = 200)
    branch = models.CharField(max_length = 200)
    fullname = models.CharField(max_length=200)
    key = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.email

class Admin(models.Model):
    hashid = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.hashid
