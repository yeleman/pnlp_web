#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, RequestContext, redirect
from django.contrib import messages
from django import forms
from django.http import Http404

from pnlp_web.http import Http403
from bolibana_reporting.models import *
from pnlp_core.models import *
from pnlp_web.utils import get_level_for


class ProviderForm(forms.Form):

    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=12, required=False)

class ProviderPasswordForm(forms.Form):
    password1 = forms.CharField(max_length=100, label="New Password")
    password2 = forms.CharField(max_length=100, label="Confirm new Password")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


@login_required
def index(request):
    provider = request.user.get_profile()

    level = get_level_for(provider)

    # forward user to his matching level
    if level == 'national':
        return index_national(request)

    if level == 'region':
        return index_region(request)

    if level == 'district':
        return index_district(request)

    return index_norole(request)


@login_required
def index_national(request):
    context = {}
    return render_to_response('index_national.html', context, RequestContext(request))


@login_required
def index_region(request):
    context = {}
    return render_to_response('index_region.html', context, RequestContext(request))


@login_required
def index_district(request):
    context = {}
    return render_to_response('index_district.html', context, RequestContext(request))


@login_required
def index_norole(request):
    #raise Http404
    return render_to_response('index.html', {}, RequestContext(request))


@login_required
def edit_profile(request):
    context = {}
    provider = request.user.get_profile()

    is_password = 'password1' in request.POST

    if request.method == 'POST' and not is_password:
        form = ProviderForm(request.POST)
        if form.is_valid() and not is_password:
            provider.first_name = form.cleaned_data.get('first_name')
            provider.last_name = form.cleaned_data.get('last_name')
            provider.email = form.cleaned_data.get('email')
            provider.phone_number = form.cleaned_data.get('phone_number')
            provider.save()
            messages.success(request, 'Profile details updated.')
            return redirect(index)
    elif is_password:
        form = ProviderForm(provider.to_dict())

    if request.method == 'POST' and is_password:
        passwd_form = ProviderPasswordForm(request.POST)
        if passwd_form.is_valid() and is_password:
            provider.set_password(passwd_form.cleaned_data.get('password1'))
            provider.save()
            messages.success(request, 'Password updated.')
            return redirect('logout')
    elif not is_password:
        passwd_form = ProviderPasswordForm()

    if request.method == 'GET':
        form = ProviderForm(provider.to_dict())
        passwd_form = ProviderPasswordForm()

    context.update({'form': form, 'passwd_form': passwd_form})

    return render_to_response('edit_profile.html', context, RequestContext(request))


def handle_uploaded_file(f):
    fname = '/tmp/form_%s.xls' % datetime.now().strftime('%s')
    destination = open(fname, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return fname


@login_required
def upload_form(request):
    context = {}
    provider = request.user.get_profile()

    if request.method == 'POST':
        if 'excel_form' in request.FILES:
            filepath = handle_uploaded_file(request.FILES['excel_form'])

            errors = None
            status = None
            instance = None

            from pnlp_core.excel import *

            form = MalariaExcelForm(filepath)
            if form.is_valid():
                try:
                    instance = form.create_report(author=provider)
                    #status = instance.status
                    status = 'ok'
                except IncorrectReportData:
                    status = 'error'
            else:
                print "NOT VALID"

            if form.errors.count() > 0:
                status = 'error'
            context.update({'all_errors': form.errors.all(True)})

            """print form
        #    print form.get('month')
            #print "\n".join(["%s: %s" % (key, value) for key, value in form.to_dict().items()])
            print form.to_dict().__len__()
            print "ERRORS (%d):" % form.errors.count()
            for section, serrors in errors.items():
                print("> %s" % section.upper())
                print("\t" + "\n\t".join([error for error in serrors]))
                #print "\n".join(form.errors.all())"""
        else:
            status = 'nofile'

        context.update({'status': status})

    return render_to_response('upload_form.html', context, RequestContext(request))
