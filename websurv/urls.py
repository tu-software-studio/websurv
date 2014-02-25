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
    url(r'^surveys/$', survey_index, name='survey_index')
)
