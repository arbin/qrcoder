from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from os import path

from qrcoder import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'qrcoder.views.home', name='home'),
    # url(r'^qrcoder/', include('qrcoder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'qrcoder.views.home', name='home'),
    url(r'^about', 'qrcoder.views.about', name='about'),
    url(r'^faqs', 'qrcoder.views.faqs', name='faqs'),
    url(r'^how-it-works', 'qrcoder.views.how_it_works', name='how-it-works'),
    url(r'^email', 'qrcoder.views.email', name='email'),
    url(r'^uploads', 'qrcoder.views.uploads', name='uploads'),
    url(r'^qr-code-logo', 'qrcoder.views.custom', name='custom'),
    url(r'^arbin', 'qrcoder.views.arbin', name='arbin'),
    url(r'^print', 'qrcoder.views.print_qr', name='print'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(path.dirname(__file__), 'media')}),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
