from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timboektu.views.home', name='home'),
    # url(r'^timboektu/', include('timboektu.foo.urls')),
    
    url(r'^timboektu/books/$', 'timboektu.books.views.index'),
    url(r'^timboektu/books/post/(?P<post_id>\d+)/$', 'timboektu.books.views.detail'),
    url(r'^timboektu/books/post/new/$', 'timboektu.books.views.new'),
    url(r'^timboektu/books/post/edit/(?P<post_hash>.+)/$', 'timboektu.books.views.edit'),
    url(r'^timboektu/books/department/(?P<department_id>\d+)/$', 'timboektu.books.views.department'),
    url(r'^timboektu/books/about/$', 'timboektu.books.views.about'),
    url(r'^timboektu/books/contact/$', 'timboektu.books.views.contact'),
    url(r'^timboektu/books/post/confirm/(?P<post_hash>.+)/$', 'timboektu.books.views.confirm'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
