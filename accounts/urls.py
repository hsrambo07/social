from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy


urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout1'),
    url(r'^profile/edit/', views.edit, name='edit'),

    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    path('change-password/', views.change_password, name='change_password'),
    url('^', include('django.contrib.auth.urls')),
    url('social-auth/', include('social_django.urls', namespace='social')),
    ###url('^accounts/register/', CreateView.as_view(
        #template_name='registration/register.html',
        #form_class=UserCreationForm,
        ##success_url=reverse_lazy('edit')  # note the usage of reverse_lazy here 
   # ), name='register'),
]  
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

