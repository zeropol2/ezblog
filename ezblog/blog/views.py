from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from .models import Post


# index
def index(request):
    per_page = 2
    page = request.GET.get('page', 1)

    pg = Paginator(Post.objects.all(), per_page)

    try:
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts': contents,
    }

    return render(request, 'list.html', ctx)
