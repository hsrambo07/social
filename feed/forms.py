from django import forms
from .models import UserPost
from django.contrib.auth.models import User
from django.utils.text import slugify



class UpdateFeedForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('post_body','image','users_like') #Note that we didn't mention user field here.

    def save(self, force_insert=False,force_update=False,commit=True):
        user_profiles = super(UpdateFeedForm, self).save(commit=False)
        if commit:
            user_profiles.save()
        return user_profiles
