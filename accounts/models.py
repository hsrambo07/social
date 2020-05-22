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





class Contact(models.Model):
    user_form =models.ForeignKey('auth.User',related_name='rel_from_set',on_delete=models.CASCADE)
    users_to=models.ForeignKey('auth.User',related_name='rel_to_set',on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_form,self.user_to)
    
following =models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False)

User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))
    
    

