from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from django.db.models.signals import post_save

class Profile(models.Model):
    image=models.ImageField(upload_to='images/')
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    bio=models.TextField()
    url=models.TextField()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

