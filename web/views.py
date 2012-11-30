# -*- coding=utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# 首页 {{{1
def v_index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


# 无权限 {{{1
def v_no_permission(request):
    return render_to_response('no_permission.html', locals(), context_instance=RequestContext(request))


# vim: foldmethod=marker
# vim: foldcolumn=2
