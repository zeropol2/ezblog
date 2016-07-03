from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Category, Tag


# index
def index(request):
    per_page = 2
    page = request.GET.get('page', 1)

    if request.user.is_authenticated():
        pg = Paginator(Post.objects.all(), per_page)
    else:
        pg = Paginator(Post.objects.filter(status='public'), per_page)

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
        url = reverse('blog:index')
        return redirect(url)
    elif request.method == 'DELETE':
        return __delete_post(request, pk)
    else:
        raise Http404


def __get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    ctx = {
        'post': post,
    }

    return render(request, 'detail.html', ctx)


def __delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    response = HttpResponse()
    response.status_code = 200
    return response


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
    tags = request.POST.get('tags').split(',')

    new_post = Post()
    new_post.title = title
    new_post.content = content
    if category_pk:
        new_post.category = Category.objects.get(pk=category_pk)
    new_post.status = status
    new_post.save()
    if tags:
        for name in tags:
            name = name.strip()
            print(name)
            try:
                tag = Tag.objects.get(name=name)
            except Tag.DoesNotExist:
                tag = Tag()
                tag.name = name
                tag.save()
            new_post.tags.add(tag)
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
