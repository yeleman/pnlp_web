#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib import admin
from pnlp_core.models import *


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
