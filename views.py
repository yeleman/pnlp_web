#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.shortcuts import (render_to_response, HttpResponseRedirect, 
                              HttpResponse)

def index(request):
	return HttpResponse("test")