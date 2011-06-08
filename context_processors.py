#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

from pnlp_web.utils import get_level_for


def add_provider(request):
    try:
        provider = request.user.get_profile()
    except:
        provider = None
    return {'provider': provider}


def add_level(request):
    try:
        level = get_level_for(request.user.get_profile())
    except:
        level = None
    return {'level': level}
