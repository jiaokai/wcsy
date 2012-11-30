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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', v_index),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    (r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url':'/login/'} ),
    (r'^password_change/$', 'django.contrib.auth.views.password_change', {'post_change_redirect':'/login/'} ),
    # (r'^help/$', v_help),
    (r'^nopermission/$', v_no_permission),
)
