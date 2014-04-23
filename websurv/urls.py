from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from thin.views import *

urlpatterns = patterns(
    '',

    url(r'^$', project_index, name='home'),
    url(r'^bread/$', home, name="breadcrumbs"),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dictionaries/(?P<id>\d+)/$', dictionary_detail, name='dictionary_detail'),
    url(r'^dictionaries/(?P<id>\d+)/edit/$', dictionary_edit, name='dictionary_edit'),
    url(r'^dictionaries/add/(?P<id>\d+)/$', dictionary_add, name='dictionary_add'),
    url(r'^dictionaries/(?P<id>\d+)/delete/$', dictionary_delete, name='dictionary_delete'),

    url(r'^surveys/(?P<id>\d+)/$', survey_detail, name='survey_detail'),
    url(r'^surveys/(?P<id>\d+)/edit/$', survey_edit, name='survey_edit'),
    url(r'^surveys/(?P<id>\d+)/delete/$', survey_delete, name='survey_delete'),
    url(r'^surveys/add/(?P<id>\d+)$', survey_add, name='survey_add'),

    url(r'^projects/$', project_index, name='project_index'),
    url(r'^projects/(?P<num>\d+)/$', project_detail, name='project_detail'),
    url(r'^projects/(?P<num>\d+)/edit/$', project_edit, name='project_edit'),
    url(r'^projects/(?P<num>\d+)/delete/$', project_delete, name='project_delete'),
    url(r'^projects/add/$', project_add, name='project_add'),

    url(r'^varieties/(?P<num>\d+)/$', variety_detail, name='variety_detail'),
    url(r'^varieties/(?P<num>\d+)/edit/$', variety_edit, name='variety_edit'),
    url(r'^varieties/(?P<num>\d+)/delete/$', variety_delete, name='variety_delete'),
    url(r'^varieties/add/$',variety_add,name='variety_add'),

    url(r'^glosses/(?P<id>\d+)/$', gloss_detail, name='gloss_detail'),
    url(r'^glosses/(?P<id>\d+)/edit/$', gloss_edit, name='gloss_edit'),
    url(r'^glosses/add/(?P<id>\d+)/$', gloss_add, name='gloss_add'),
    url(r'^glosses/add/(?P<id>\d+)/submit$', gloss_add_with_ajax, name='gloss_add_with_ajax'),
    url(r'^glosses/(?P<id>\d+)/delete/$', gloss_delete, name='gloss_delete'),

    url(r'^comparisons/(?P<num>\d+)/$', comparison_detail, name='comparison_detail'),
    url(r'^comparisons/(?P<num>\d+)/edit/$', comparison_edit, name='comparison_edit'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'thin/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : project_index},  name='logout'),

)
