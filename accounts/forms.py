from django import forms
from .models import Profile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'url','image') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'url','image') #Note that we didn't mention user field here.

    def clean_email(self):
        bio = self.cleaned_data.get('bio')
        url = self.cleaned_data.get('url')
        image = self.cleaned_data.get('image')

        

    def save(self, commit=True):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile       

class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email')  

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image','bio','url')        
