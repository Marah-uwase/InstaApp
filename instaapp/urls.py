from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

 # So we can use it like: {% url 'mymodule:user_register' %} on our template. 
urlpatterns = [
    
    url(r'^home/$', views.home, name='home'),
    url(r'^$',views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^user/(?P<username>\w{0,50})',views.profile,name='profile'),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^accounts/edit/',views.edit_profile, name='edit_profile'),
    url(r'^image/(?P<image_id>\d+)', views.single_image, name='single_image'),
    url('search/', views.search_profiles, name='search'),
    url('unfollow/<unfollowing>', views.unfollow, name='unfollow'),
    url('follow/<following>', views.follow, name='follow'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
