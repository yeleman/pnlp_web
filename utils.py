#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from django.contrib.auth.models import ContentType

from bolibana_reporting.models import Access, Role


def get_level_for(provider):
    # finds best access
    # based on number of descendants
    # in the entities hierarchy
    best_access = provider.best_access() or \
                  Access.objects.get(role=Role.objects.get(slug='guest'), \
                  object_id=1, \
                  content_type=ContentType.objects.get(\
                               app_label='bolibana_reporting', model='entity'))

    return best_access.target.type.slug
