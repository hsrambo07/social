from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    image=models.ImageField(upload_to='images/')
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    bio=models.TextField()
    url=models.TextField()


def __str__(self):
    return self.title


def pub_date_pretty(self):
    return self.pub_date.strftime('%b  %e  %y')

def summary(self):
    return self.body[:100]
