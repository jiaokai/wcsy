# -*- coding=utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from wcsy.web.models import *
import re

# 通用函数 {{{1
# 分页 {{{2
def g_pages(records, per, page, ):
    paginator = Paginator(records, per)

    # try:
        # page = int(request.GET.get('page', '1'))
    # except:
        # page = 1
    after_range_num = 5        #当前页前显示5页
    befor_range_num = 4       #当前页后显示4页
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+befor_range_num]
    if page_range[0] > 2:
        page_range.insert(0, 1)
        page_range.insert(1, '...')
    if page_range[-1] < (paginator.page_range[-1] - 1):
        page_range.append('...')
        page_range.append(paginator.page_range[-1])

    try:
        records_result = paginator.page(page)
    except:
        records_result = paginator.page(paginator.num_pages) #}}}4

    return records_result

# 首页 {{{1
def v_index(request):
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

# 新闻 {{{1
def v_news(request):
    category = request.GET.get('category', '1')
    t_title = m_news.CATEGORY[int(category)-1][1]
    news = m_news.objects.filter(i_status__lte=5, i_category=int(category))

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    news = g_pages(news, 2, page)
    return render_to_response('news.html', locals(), context_instance=RequestContext(request))

def v_news_content(request):
    tid = int(request.GET.get('tid', '0'))
    if tid > 0:
        try:
            t_news = m_news.objects.get(pk=tid)
        except:
            return HttpResponseRedirect('/news/')
    return render_to_response('news_content.html', locals(), context_instance=RequestContext(request))
# 产品 {{{1
def v_product(request):
    categorys = m_product_category.objects.all()
    try:
        category = int(request.GET.get('category', '0'))
    except:
        category = 0
    if category == 0:
        t_title = u"全部产品"
        products = m_product.objects.all()
    else:
        try:
            t_category = m_product_category.objects.get(pk=category)
        except:
            return HttpResponseRedirect('/product/')
        else:
            t_title = t_category.s_cname
            products = m_product.objects.filter(f_category=t_category)

    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    products = g_pages(products, 2, page)
    return render_to_response('product.html', locals(), context_instance=RequestContext(request))

# 公司简介 {{{1
def v_company(request):
    try:
        company = m_options.objects.get(s_name="company")
    except:
        pass
    return render_to_response('company.html', locals(), context_instance=RequestContext(request))
# 人事招聘 {{{1
def v_hire(request):
    try:
        hire = m_options.objects.get(s_name="hire")
    except:
        pass
    return render_to_response('hire.html', locals(), context_instance=RequestContext(request))
# 联系我们 {{{1
def v_contact(request):
    try:
        contact = m_options.objects.get(s_name="contact")
    except:
        pass
    return render_to_response('contact.html', locals(), context_instance=RequestContext(request))

def v_product_content(request):
    categorys = m_product_category.objects.all()
    tid = int(request.GET.get('tid', '0'))
    if tid > 0:
        try:
            t_product = m_product.objects.get(pk=tid)
        except:
            return HttpResponseRedirect('/product/')
    return render_to_response('product_content.html', locals(), context_instance=RequestContext(request))

# 无权限 {{{1
def v_no_permission(request):
    return render_to_response('no_permission.html', locals(), context_instance=RequestContext(request))

# admins {{{1
# admin {{{2
@login_required
def v_admin( request ):
    return render_to_response('admin.html', locals(), context_instance=RequestContext(request))
# admin-news 列表页面 {{{2
@login_required
def v_admin_news( request ):
    news = m_news.objects.all()
    return render_to_response('admin_news.html', locals(), context_instance=RequestContext(request))
# admin-news 编辑页面 {{{2
@login_required
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
                face = re.findall(r'src=".*?"', cd['s_content'])
                if face:
                    face = face[0]
                else:
                    face = ""
                t_news = m_news(s_title=cd['s_title'], s_sum=cd['s_sum'], s_content=cd['s_content'], i_status=1, s_poster='dd', s_face=face)
                t_news.save()
                return HttpResponseRedirect('/admin/news/')
            else:
                t_news.s_title = cd['s_title']
                t_news.s_sum = cd['s_sum']
                t_news.s_content = cd['s_content']
                face = re.findall(r'src=".*?"', cd['s_content'])
                if face:
                    t_news.s_face = face[0]
                t_news.save()
                return HttpResponseRedirect('/admin/news/')

    return render_to_response('admin_news_edit.html', locals(), context_instance=RequestContext(request))

# admin 产品 {{{2
@login_required
def v_admin_product( request ):
    products = m_product.objects.all()
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    products = g_pages(products, 10, page)
    return render_to_response('admin_product.html', locals(), context_instance=RequestContext(request))
@login_required
def v_admin_product_edit( request ):
    tid = request.GET.get('tid', '')
    action = request.GET.get('action', '')
    if tid != '':
        try:
            t_product = m_product.objects.get(pk=tid)
        except:
            messages.error(request, u"无此产品！")
            return HttpResponseRedirect('/admin/product/')
        else:
            if action == 'delete':
                t_product.delete()
                messages.info(request, u"产品删除成功！")
                return HttpResponseRedirect('/admin/product/')
    if request.method == 'GET':
        if tid == '':
            f = f_product()
        else:
            f = f_product(initial={'f_category':t_product.f_category, \
                                   # 'd_postdate': t_product.d_postdate, \
                                   's_name':t_product.s_name, \
                                   'i_price':t_product.i_price, \
                                   's_intr': t_product.s_intr, \
                                   's_link_buy': t_product.s_link_buy })

    elif request.method == 'POST':
        f = f_product(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            if tid == '':
                face = re.findall(r'src=".*?"', cd['s_intr'])
                if face:
                    face = face[0]
                else:
                    face = ""
                t_product = m_product(f_category=cd['f_category'], \
                                      s_name=cd['s_name'], \
                                      i_price=cd['i_price'], \
                                      s_intr=cd['s_intr'], \
                                      s_face=face, \
                                      s_link_buy=cd['s_link_buy'], \
                                      i_status=1, \
                                      s_poster=request.user.username )
                t_product.save()
                return HttpResponseRedirect('/admin/product/')
            else:
                t_product.f_category = cd['f_category']
                t_product.s_name = cd['s_name']
                t_product.i_price = cd['i_price']
                t_product.s_intr = cd['s_intr']
                t_product.s_link_buy = cd['s_link_buy']
                t_product.s_poster = request.user.username

                face = re.findall(r'src=".*?"', cd['s_intr'])
                if face:
                    t_product.s_face = face[0]
                t_product.save()
                return HttpResponseRedirect('/admin/product/')

    return render_to_response('admin_product_edit.html', locals(), context_instance=RequestContext(request))

@login_required
def v_admin_product_category( request ):
    categorys = m_product_category.objects.all()
    return render_to_response('admin_product_category.html', locals(), context_instance=RequestContext(request))

@login_required
def v_admin_product_category_edit( request ):
    tid = request.GET.get('tid', '')
    action = request.GET.get('action', '')
    if tid != '':
        try:
            t_category = m_product_category.objects.get(pk=tid)
        except:
            messages.error(request, u"无此分类！")
            return HttpResponseRedirect('/admin/product/category/')
        else:
            if action == 'delete':
                t_category.delete()
                messages.info(request, u"分类删除成功！")
                return HttpResponseRedirect('/admin/product/category/')
    if request.method == 'GET':
        if tid == '':
            f = f_product_category()
        else:
            f = f_product_category(initial={'s_cname':t_category.s_cname, 's_sum':t_category.s_sum})

    elif request.method == 'POST':
        f = f_product_category(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            if tid == '':
                t_category = m_product_category(s_cname=cd['s_cname'], s_sum=cd['s_sum'])
                t_category.save()
                return HttpResponseRedirect('/admin/product/category/')
            else:
                t_category.s_cname = cd['s_cname']
                t_category.s_sum = cd['s_sum']
                t_category.save()
                return HttpResponseRedirect('/admin/product/category/')
    return render_to_response('admin_product_category_edit.html', locals(), context_instance=RequestContext(request))

# admin 公司简介 {{{2
@login_required
def v_admin_company( request ):
    try:
        company = m_options.objects.get(s_name=u"company")
    except:
        if request.method == "GET":
            f = f_options()
        elif request.method == "POST":
            f = f_options(request.POST)
            if f.is_valid():
                cd = f.cleaned_data
                m_options(s_name=u"company", s_content=cd['s_content'], i_status=1).save()
    else:
        if request.method == "GET":
            f = f_options(initial={'s_name':company.s_name, 's_content': company.s_content})
        elif request.method == "POST":
            f = f_options(request.POST)
            if f.is_valid():
                cd = f.cleaned_data
                company.s_content = cd['s_content']
                company.save()
    return render_to_response('admin_company.html', locals(), context_instance=RequestContext(request))

# admin 人事招聘 {{{2
@login_required
def v_admin_hire( request ):
    try:
        hire = m_options.objects.get(s_name="hire")
    except:
        f = f_options()
    else:
        f = f_options(initial={'s_name':hire.s_name, 's_content': hire.s_content})
    return render_to_response('admin_hire.html', locals(), context_instance=RequestContext(request))

# admin 联系我们 {{{2
@login_required
def v_admin_contact( request ):
    try:
        contact = m_options.objects.get(s_name="contact")
    except:
        f = f_options()
    else:
        f = f_options(initial={'s_name':contact.s_name, 's_content': contact.s_content})
    return render_to_response('admin_contact.html', locals(), context_instance=RequestContext(request))

# vim: foldmethod=marker
# vim: foldcolumn=2
