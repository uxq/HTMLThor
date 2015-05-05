from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^', include('htmlthorapp.urls')),
                       url(r'^admin/', include(admin.site.urls))
)
urlpatterns += staticfiles_urlpatterns()
#urlpatterns += patterns('django.contrib.staticfiles.views',
#			url(r'^(?P<path>.*)$', 'serve'),)
