#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from bolibana_reporting.models import *
from bolibana_reporting.admin import *
from bolibana_auth.models import *
from pnlp_core.models import *


class ProviderUserStacked(admin.StackedInline):
    model = Provider
    fk_name = 'user'
    max_num = 1


class CustomUserAdmin(UserAdmin):
    inlines = [ProviderUserStacked,]

class MalariaReportAdmin(admin.ModelAdmin):    
    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('receipt',) + self.readonly_fields
        return self.readonly_fields


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(MalariaReport, MalariaReportAdmin)
admin.site.register(Period)
admin.site.register(Entity, EntityAdmin)
admin.site.register(EntityType)
admin.site.register(Provider)
admin.site.register(Role)
admin.site.register(Access)
admin.site.register(Permission)
