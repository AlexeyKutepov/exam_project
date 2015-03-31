__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from authentication import views

urlpatterns = patterns('',
        url(r'^login/$', views.sign_in, name='login'),
        url(r'^logout/$', views.sign_out, name='logout'),
        url(r'^create/profile/$', views.create_profile, name='create_profile'),
)