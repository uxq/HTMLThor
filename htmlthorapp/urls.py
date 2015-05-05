from django.conf.urls import patterns, url
from htmlthorapp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^thorpedoFile/$', views.thorpedoFile, name='thorpedoFile'),
                       url(r'^thorpedoUrl/$', views.thorpedoUrl, name='thorpedoUrl'),
                       url(r'^thorpedoDirect/$', views.thorpedoDirect, name='thorpedoDirect'))


