from django.contrib import admin

# Register your models here.
from .models import UserPost
list_display=['post_body','slug','image','post_date']
list_filter=['post_date']
admin.site.register(UserPost)
