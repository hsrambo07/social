from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models.signals import post_save

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='images/',blank='True')

    bio=models.TextField()
    url=models.TextField()
    #gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    #phone= models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return u"%s" % self.user.username
