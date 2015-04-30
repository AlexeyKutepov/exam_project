__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from exam import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^dashboard/results/', views.dashboard_results, name='dashboard_results'),
        url(r'^dashboard/', views.dashboard, name='dashboard'),
        url(r'^journal/(?P<id>\d+)/$', views.journal, name='journal'),
        url(r'^create_new_test/', views.create_new_test, name='create_new_test'),
        url(r'^create_new_question/(?P<id>\d+)/$', views.create_new_question, name='create_new_question'),
        url(r'^tests/(?P<page>\d+)/(?P<search>.+)/$', views.get_test_list_search, name='get_test_list_search'),
        url(r'^tests/(?P<page>\d+)/$', views.get_test_list, name='get_test_list'),
        url(r'^start_test/', views.start_test, name='start_test'),
        url(r'^next_question/(?P<id>\d+)/(?P<number>\d+)/$', views.next_question, name='next_question'),
        url(r'^end_test/(?P<id>\d+)/$', views.end_test, name='end_test'),
)