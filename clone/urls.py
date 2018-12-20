# from django.shortcuts import render
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    url(r'^$', views.hello, name='hello'),
    url(r'signup/', views.signup, name='signup'),
    url(r'^view_profile/', views.view_profile, name='profile'),
    url(r'^edit_profile/', views.edit_profile, name='edit_profile'),
    url(r'^upload_image/', views.upload_image, name='upload_image'),
    url(r'^search_user/', views.search_user, name='search_user'),
    url(r'^new_comment/(\d+)', views.new_comment, name='new_comment'),
    url(r'^single_image/(\d+)', views.single_image, name='single_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
