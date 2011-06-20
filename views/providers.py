#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext
from django.utils.translation import ugettext as _, ugettext_lazy


class EditProviderForm(forms.Form):

    first_name = forms.CharField(max_length=50, required=False, \
                                 label=ugettext_lazy(u"First Name"))
    last_name = forms.CharField(max_length=50, required=False, \
                                label=ugettext_lazy(u"Last Name"))
    email = forms.EmailField(required=False, \
                             label=ugettext_lazy(u"E-mail Address"))
    phone_number = forms.CharField(max_length=12, required=False, \
                                   label=ugettext_lazy(u"Phone Number"))


@login_required
def list_users(request):
    return render_to_response('upload_form.html', \
                              context, RequestContext(request))


def add_user(request):
    return


def edit_user(request, user_id):
    return


def disable_user(request, user_id):
    return
