from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from thin.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'websurv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dictionaries/$', dictionary_index, name='dictionary_index'),

    url(r'^surveys/(?P<pk>\d+)/edit/$', survey_edit, name='survey_edit'),

    url(r'^projects/$', project_index, name='project_index'),
    url(r'^projects/(?P<num>\d+)/$', project_detail, name='project_detail'),
    url(r'^projects/(?P<num>\d+)/edit/$', project_edit, name='project_edit'),

)
