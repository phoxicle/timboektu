from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timboektu.views.home', name='home'),
    # url(r'^timboektu/', include('timboektu.foo.urls')),
    
    url(r'^$', 'timboektu.books.views.index'),
    url(r'^post/(?P<post_id>\d+)/$', 'timboektu.books.views.detail'),
    url(r'^post/new/$', 'timboektu.books.views.new'),
    url(r'^post/edit/(?P<post_hash>.+)/$', 'timboektu.books.views.edit'),
    url(r'^post/renew/(?P<post_hash>.+)/$', 'timboektu.books.views.renew'),
    url(r'^department/(?P<department_id>\d+)/$', 'timboektu.books.views.department'),
    url(r'^about/$', 'timboektu.books.views.about'),
    url(r'^contribute/$', 'timboektu.books.views.contribute'),
    url(r'^post/confirm/(?P<post_hash>.+)/$', 'timboektu.books.views.confirm'),
    url(r'^delete/$', 'timboektu.books.views.delete'),
    url(r'^locations/$', 'timboektu.books.views.locations'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
