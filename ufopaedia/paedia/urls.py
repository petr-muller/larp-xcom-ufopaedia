from django.conf.urls import patterns, url

from paedia import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^category/(?P<category_id>\d+)/$', views.article_view),
  url(r'^category/(?P<category_id>\d+)/article/(?P<article_id>\d+)/$', views.article_view, name="article_view"),
  url(r'^unlock/$', views.unlock, name="unlock"),
  url(r'^research/$', views.research, name='research'),
)
