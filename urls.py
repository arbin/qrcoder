from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from os import path

from qrcoder import settings

urlpatterns = patterns('',
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
