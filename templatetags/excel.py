#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='pnlpcat')
@stringfilter
def formcategories(value):
    value = value.lower()
    if value == 'u5':
        return u"Children Under 5yo."
    if value == 'o5':
        return u"Children Over 5yo."
    if value == 'pw':
        return u"Pregnant Women"
    if value == 'period':
        return u"Reporting"
    if value == 'fillin':
        return u"Collect / Data Entry"
    if value == 'stockout':
        return u"Stock outs"
