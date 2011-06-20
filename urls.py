#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import os

from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.views.generic import DetailView, ListView

from pnlp_web import views
from settings import STATIC_ROOT
from bolibana_auth.models import Provider

ENTITY_TIME_REGEX = r'(?P<entity_code>[a-z0-9A-Z\.\_\-]+)/' \
                     'from(?P<from_m>[0-9]{2})(?P<from_y>[0-9]{4})' \
                     'to(?P<to_m>[0-9]{2})(?P<to_y>[0-9]{4})'

urlpatterns = patterns('',
    url(r'^/?$', views.dashboard.index, name='index'),
    url(r'^profile/$', views.profile.edit_profile, name='profile'),

    # login
    url(r'^login/$', 'django.contrib.auth.views.login', \
         {'template_name': 'login_django.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', \
         {'template_name': 'logout_django.html'}, name='logout'),

    # district
    url(r'^upload/$', views.excel_upload.upload_form, name='upload'),

    # ANTIM
    url(r'^users/$', views.providers.list_users, name='list_users'),
    url(r'^users/add$', views.providers.add_user, name='add_user'),
    url(r'^users/edit/(?P<user_id>[0-9]+)$', \
        views.providers.edit_user, name='edit_user'),
    url(r'^users/disable/(?P<user_id>[0-9]+)$', \
        views.providers.disable_user, name='disable_user'),

    url(r'^auto$', ListView.as_view(
            queryset=Provider.objects.order_by('user__first_name', \
                                               'user__last_name')[:50],
            context_object_name='users_list',
            template_name='users_list.html')),

    # static web pages
     url(r'^support/$', direct_to_template, \
         {'template': 'support.html'}, name='support'),
     url(r'^help/$', direct_to_template, \
         {'template': 'help.html'}, name='help'),
     url(r'^about/$', direct_to_template, \
         {'template': 'about.html'}, name='about'),

    # development only
    url(r'^static/admin/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': os.path.join(os.path.dirname(\
                                            os.path.abspath(admin.__file__)), \
                               'media'), 'show_indexes': True}, \
             name='static_admin'),

    url(r'^static/(?P<path>.*)$',
             'django.views.static.serve',
             {'document_root': STATIC_ROOT, 'show_indexes': True}, \
             name='static'),
)
