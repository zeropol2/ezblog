from django.conf.urls import url

from blog import views

app_name = 'blog'

urlpatterns = [
    url(r'^posts/(?P<pk>[0-9]+)/$', views.posts, name='posts'),
    url(r'^posts/$', views.create_post, name='create_post'),
    url(r'^$', views.index, name='index'),
]
