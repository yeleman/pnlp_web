#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from bolibana_reporting.models import *
from bolibana_auth.models import *
from pnlp_core.models import *


class ProviderUserStacked(admin.StackedInline):
    model = Provider
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [ProviderUserStacked,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(MalariaReport)
admin.site.register(Period)
admin.site.register(Entity)
admin.site.register(EntityType)
admin.site.register(MalariaUnderFiveReport)
admin.site.register(MalariaOverFiveReport)
admin.site.register(MalariaPregnantWomenReport)
admin.site.register(MalariaStockOutsReport)
admin.site.register(Provider)
admin.site.register(Role)
admin.site.register(Access)
admin.site.register(Permission)
