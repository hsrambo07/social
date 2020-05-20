from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class UserPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userpost', null=True, on_delete=models.CASCADE)
    post_body = models.TextField(blank=True, null=True, default='Whats happening?')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    post_date = models.DateTimeField(auto_now_add=True,db_index=True)
    users_like=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="images_liked",blank=True)
    slug=models.SlugField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.post_date)
        super(UserPost,self).save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('images:detail',args=[self.id,self.slug])   

    
