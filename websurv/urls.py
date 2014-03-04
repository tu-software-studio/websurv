from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from thin.views import *

# TODO - Separate app-specific URLs to apps themselves.

urlpatterns = patterns(
    '',

    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dictionaries/$', dictionary_index, name='dictionary_index'),
    url(r'^dictionaries/(?P<id>\d+)/$', dictionary_detail, name='dictionary_detail'),
    url(r'^dictionaries/(?P<id>\d+)/edit/$', dictionary_edit, name='dictionary_edit'),

    url(r'^surveys/$', survey_index, name='survey_index'),
    url(r'^surveys/(?P<pk>\d+)/$', survey_detail, name='survey_detail'),
    url(r'^surveys/(?P<pk>\d+)/edit/$', survey_edit, name='survey_edit'),

    url(r'^projects/$', project_index, name='project_index'),
    url(r'^projects/(?P<num>\d+)/$', project_detail, name='project_detail'),
    url(r'^projects/(?P<num>\d+)/edit/$', project_edit, name='project_edit'),
    url(r'^projects/(?P<num>\d+)/delete/$', project_delete, name='project_delete'),
    url(r'^projects/add/$', project_add, name='project_add'),

    url(r'^varieties/$', variety_index, name='variety_index'),
    url(r'^varieties/(?P<num>\d+)/$', variety_detail, name='variety_detail'),
    url(r'^varieties/(?P<num>\d+)/edit/$', variety_edit, name='variety_edit'),

    url(r'^comparisons/$', comparison_index, name='comparison_index'),
    url(r'^comparisons/(?P<num>\d+)/$', comparison_detail, name='comparison_detail'),
    url(r'^comparisons/(?P<num>\d+)/edit/$', comparison_edit, name='comparison_edit'),
)
