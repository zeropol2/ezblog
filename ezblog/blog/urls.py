from django.conf.urls import url

from blog import views

app_name = 'blog'

urlpatterns = [
    url(r'^posts/(?P<pk>[0-9]+)/update/$', views.update_post_form, name='update_post_form'),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.post, name='post'),
    url(r'^posts/create/$', views.create_post_form, name='create_post_form'),
    url(r'^posts/tag/(?P<tag_pk>[0-9]+)/$', views.posts_by_tag, name='posts_by_tag'),
    url(r'^posts/category/(?P<category_pk>[0-9]+)/$', views.posts_by_category, name='posts_by_category'),
    url(r'^posts/keyword/$', views.posts_by_keyword, name='posts_by_keyword'),
    url(r'^posts/$', views.create_post_or_list_posts, name='create_post_or_list_posts'),
    url(r'^$', views.index, name='index'),
]
