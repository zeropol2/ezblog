from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Category


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
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        raise Http404

    url = reverse('blog:index')
    return redirect(url)


def __get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    ctx = {
        'post': post,
    }

    return render(request, 'detail.html', ctx)


# create_post
def create_post(request):
    if request.method == 'GET':
        return __create_form(request)
    elif request.method == 'POST':
        return __create_post(request)
    else:
        raise Http404


def __create_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    category_pk = request.POST.get('category')
    status = request.POST.get('status')

    new_post = Post()
    new_post.title = title
    new_post.content = content
    if category_pk:
        new_post.category = Category.objects.get(pk=category_pk)
    new_post.status = status
    new_post.save()

    url = reverse('blog:posts', kwargs={'pk': new_post.pk})
    return redirect(url)


def __create_form(request):
    categories = Category.objects.all()
    post = Post()
    status_choices = post.get_status_choices()
    ctx = {
        'categories': categories,
        'status_choices': status_choices,
    }

    return render(request, 'edit.html', ctx)
