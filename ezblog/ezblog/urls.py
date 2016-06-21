from django.conf.urls import url, include
from django.contrib import admin
app_name = 'blog'
urlpatterns = [
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
]
