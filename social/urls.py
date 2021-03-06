from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('feed/',include(('feed.urls','feed'), namespace='images')),
    path('',views.home,name='home'),
    path('game/',views.game,name='game'),
    path('about/',views.about,name='about'),
    path('messages/', include('communications.urls')),

] 
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

