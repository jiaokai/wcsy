from django.conf.urls.defaults import patterns, include, url

from wcsy.web.views import *
from django.conf import settings

from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wcsy.views.home', name='home'),
    # url(r'^wcsy/', include('wcsy.foo.urls')),
    url(r'ueditor/', include('DjangoUeditor.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', v_index),
    (r'^news/$', v_news),
    (r'^news/content/$', v_news_content),

    (r'^product/$', v_product),
    (r'^product/content/$', v_product_content),
    (r'^company/$', v_company),
    (r'^hire/$', v_hire),
    (r'^contact/$', v_contact),

    (r'^admin/$', v_admin),
    (r'^admin/news/$', v_admin_news),
    (r'^admin/news/edit/$', v_admin_news_edit),

    (r'^admin/product/$', v_admin_product),
    (r'^admin/product/edit/$', v_admin_product_edit),
    (r'^admin/product/category/$', v_admin_product_category),
    (r'^admin/product/category/edit/$', v_admin_product_category_edit),
    (r'^admin/company/$', v_admin_company),
    (r'^admin/hire/$', v_admin_hire),
    (r'^admin/contact/$', v_admin_contact),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/login/'} ),
    (r'^password_change/$', 'django.contrib.auth.views.password_change', {'post_change_redirect':'/login/'} ),
    # (r'^help/$', v_help),
    (r'^nopermission/$', v_no_permission),
)
