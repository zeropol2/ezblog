from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

app_name = 'blog'
urlpatterns = [
    url(r'^login/$', login,
        name='login_url',
        kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', logout,
        name='logout_url',
        kwargs={'next_page': '/login/'}),

    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
]
