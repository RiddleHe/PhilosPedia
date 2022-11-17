from django.urls import re_path

from . import views

app_name = 'pedia'

urlpatterns = [
    # url of index page
    re_path(r'^$', views.index, name='index'),
    # url of search page
    re_path(r'^search/$', views.SearchResultsView.as_view(), name='search_results'),
    # url of topics page
    re_path(r'^topics/$', views.topics, name='topics'),
    # url of individual topic page
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # url of add_topic page
    re_path(r'^add_topic/$', views.add_topic, name='add_topic'),
    # url of add_entry page
    re_path(r'^add_entry/(?P<topic_id>\d+)/$', views.add_entry, name='add_entry'),
    # url of edit_entry page
    re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]