from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

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


# posts
def posts(request, pk):
    if request.method == 'GET':
        return __get_post(request, pk)
    elif request.method == 'POST':
        raise Http404
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

    url = reverse('blog:index')
    return redirect(url)


def __get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    ctx = {
        'post': post,
    }

    return render(request, 'detail.html', ctx)



