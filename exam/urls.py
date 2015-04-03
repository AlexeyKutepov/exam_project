__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from exam import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^dashboard/', views.dashboard, name='dashboard'),
        url(r'^create_new_test/', views.create_new_test, name='create_new_test'),
)