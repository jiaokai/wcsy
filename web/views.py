# -*- coding=utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from wcsy.web.models import *

# 首页 {{{1
def v_index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


# 无权限 {{{1
def v_no_permission(request):
    return render_to_response('no_permission.html', locals(), context_instance=RequestContext(request))

# admins {{{1

# admin {{{2
def v_admin( request ):
    return render_to_response('admin.html', locals(), context_instance=RequestContext(request))
# admin-news 列表页面 {{{2
def v_admin_news( request ):
    news = m_news.objects.all()
    return render_to_response('admin_news.html', locals(), context_instance=RequestContext(request))
# admin-news 编辑页面 {{{2
def v_admin_news_edit( request ):
    tid = request.GET.get('tid', '')
    action = request.GET.get('action', '')
    if tid != '':
        try:
            t_news = m_news.objects.get(pk=tid)
        except:
            messages.error(request, u"无此新闻内容！")
            return HttpResponseRedirect('/admin/news/')
        else:
            if action == 'delete':
                t_news.delete()
                messages.info(request, u"新闻删除成功！")
                return HttpResponseRedirect('/admin/news/')
    if request.method == 'GET':
        if tid == '':
            f = f_news()
        else:
            f = f_news(initial={'s_title':t_news.s_title, 's_content':t_news.s_content})

    elif request.method == 'POST':
        f = f_news(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            if tid == '':
                t_news = m_news(s_title=cd['s_title'], s_content=cd['s_content'], i_status=1, s_poster='dd')
                t_news.save()
                return HttpResponseRedirect('/admin/news/')
            else:
                t_news.s_title = cd['s_title']
                t_news.s_content = cd['s_content']
                t_news.save()
                return HttpResponseRedirect('/admin/news/')

    return render_to_response('admin_news_edit.html', locals(), context_instance=RequestContext(request))

# vim: foldmethod=marker
# vim: foldcolumn=2
