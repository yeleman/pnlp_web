#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import forms
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, RequestContext, redirect
from django.utils.translation import ugettext as _, ugettext_lazy
from mptt.fields import TreeNodeChoiceField

from bolibana_auth.models import Role, Provider, Access
from bolibana_auth.utils import username_from_name, random_password
from bolibana_reporting.models import Entity

from pnlp_core.utils import send_email, full_url


class EditProviderForm(forms.Form):

    first_name = forms.CharField(max_length=50, required=True, \
                                 label=ugettext_lazy(u"First Name"))
    last_name = forms.CharField(max_length=50, required=True, \
                                label=ugettext_lazy(u"Last Name"))
    email = forms.EmailField(required=False, \
                             label=ugettext_lazy(u"E-mail Address"))
    phone_number = forms.CharField(max_length=12, required=False, \
                                   label=ugettext_lazy(u"Phone Number"))

    role = forms.ChoiceField(label=ugettext_lazy(u"Role"), \
                             choices=[(role.slug, role.name) \
                                      for role \
                                      in Role.objects.all().order_by('name')])

    entity = TreeNodeChoiceField(queryset=Entity.tree.all(), \
                                 level_indicator=u'---', \
                                 label=ugettext_lazy(u"Entity"))


@login_required
def list_users(request):
    context = {}
    return render(request, 'users_list.html', context)

@login_required
def add_edit_user(request, user_id=None):
    context = {}
    web_provider = request.user.get_profile()

    if request.method == 'POST':

        form = EditProviderForm(request.POST)
        if form.is_valid():

            # build an Access based on Role and Entity selected
            role = Role.objects.get(slug=form.cleaned_data.get('role'))
            entity = form.cleaned_data.get('entity')
            access = Access.find_by(role, entity)

            if user_id:
                provider = Provider.objects.get(id=user_id)
                # remove all access and add new one
                while provider.access.count() > 0 \
                      and access != provider.access.all()[0]:
                    provider.access.remove(provider.access.all()[0])
                provider.access.add(access)
            else:
                # forge username
                username = username_from_name(\
                                         form.cleaned_data.get('first_name'), \
                                         form.cleaned_data.get('last_name'))
                # generate password
                password = random_password()

                # create Provider
                provider = Provider.create_provider(username, \
                                                    password, access=[access])
            # we have a valid provider whatever the case. update details
            provider.first_name = form.cleaned_data.get('first_name')
            provider.last_name = form.cleaned_data.get('last_name')
            provider.email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            # only update if not None to preserve uniqueness
            if phone_number:
                provider.phone_number = phone_number
            provider.save()
            messages.success(request, _(u"Profile details updated."))

            if not user_id and provider.email:
                # send email with password on account creation
                sent, sent_message = send_email(recipients=provider.email, \
                                            context={'provider': provider, \
                                                     'creator': web_provider, \
                                                     'password': password, \
                                                     'url': full_url()},
                                           template='emails/new_account.txt', \
                                 title_template='emails/title.new_account.txt')
                if sent:
                    messages.success(request, _(u"An e-mail containing the " \
                                                "password has been sent " \
                                                "to %(email)s") \
                                              % {'email': provider.email})
                else:
                    messages.error(request, _(u"Unable to send e-mail " \
                                              "to %(email)s. Please record " \
                                              "and forward the password: " \
                                              "%(pass)s") \
                                            % {'email': provider.email, \
                                               'pass': password})
                    # log exception: sent_message
            # display password if user has no email address
            elif not provider.email:
                messages.info(request, _(u"Please record and forward the " \
                                         "generated password: %(pass)s") \
                                       % {'pass': password})

            return redirect(add_edit_user, provider.id)

    else:
        if user_id:
            # user_id might be forged and thus innexistant
            try:
                provider = Provider.objects.get(id=user_id)
                provider_data = provider.to_dict()
            except Provider.DoesNotExist:
                raise Http404
            try:
                provider_data.update({'entity': provider.default_access() \
                                                        .target.id, \
                                      'role': provider.main_role().slug})
            except:
                pass
        else:
            provider = {}
            provider_data = {}

        form = EditProviderForm(initial=provider_data)

    context.update({'form': form, 'user_id': user_id, 'provider': provider})

    return render(request, 'add_edit_provider.html', context)


def edit_user(request, user_id):
    return


def disable_user(request, user_id):
    return
