#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.conf.urls.defaults import patterns, include, url

from pnlp_web import views

urlpatterns = patterns('',
    url(r'^/?$', views.index),
)