from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Category, Tag


# index
def index(request):
    if request.method == 'GET':
        per_page = 2
        page = request.GET.get('page', 1)

        if request.user.is_authenticated():
            pg = Paginator(Post.objects.all(), per_page)
        else:
            pg = Paginator(Post.objects.filter(status='public'), per_page)

        return __render_index(request, pg, page)
    else:
        raise Http404


# posts
def post(request, pk):
    if request.method == 'GET':
        return __get_post(request, pk)
    elif request.method == 'PUT':
        return __update_post(request, pk)
    elif request.method == 'DELETE':
        return __delete_post(request, pk)
    else:
        raise Http404


def __get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    ctx = {
        'post': post,
        'categories': Category.objects.all()
    }

    return render(request, 'detail_post.html', ctx)


@login_required
def __update_post(request, pk):
    title = request.PUT.get('title')
    content = request.PUT.get('content')
    category_pk = request.PUT.get('category')
    status = request.PUT.get('status')
    tags = request.PUT.get('tags')
    if tags:
        tags = request.PUT.get('tags').split(',')

    post = get_object_or_404(Post, pk=pk)
    post.title = title
    post.content = content
    if category_pk:
        post.category = Category.objects.get(pk=category_pk)
    post.status = status
    post.save()
    if tags:
        for name in tags:
            name = name.strip()
            if name:
                try:
                    tag = Tag.objects.get(name=name)
                except Tag.DoesNotExist:
                    tag = Tag()
                    tag.name = name
                    tag.save()
                post.tags.add(tag)
            post.save()

    response = HttpResponse()
    response.status_code = 200
    return response


@login_required
def __delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    response = HttpResponse()
    response.status_code = 200
    return response


# create_post
def create_post_or_list_posts(request):
    if request.method == 'POST':
        return __create_post(request)
    elif request.method == 'GET':
        return index(request)
    else:
        raise Http404


@login_required
def __create_post(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    category_pk = request.POST.get('category')
    status = request.POST.get('status')
    tags = request.POST.get('tags')
    if tags:
        tags = request.POST.get('tags').split(',')

    new_post = Post()
    new_post.title = title
    new_post.content = content
    if category_pk:
        new_post.category = Category.objects.get(pk=category_pk)
    new_post.status = status
    new_post.user = request.user
    new_post.save()
    if tags:
        for name in tags:
            name = name.strip()
            if name:
                try:
                    tag = Tag.objects.get(name=name)
                except Tag.DoesNotExist:
                    tag = Tag()
                    tag.name = name
                    tag.save()
                new_post.tags.add(tag)
        new_post.save()

    url = reverse('blog:post', kwargs={'pk': new_post.pk})
    return redirect(url)


# create_post_form
@login_required
def create_post_form(request):
    if request.method == 'GET':
        return __create_post_form(request)
    else:
        raise Http404


@login_required
def __create_post_form(request):
    categories = Category.objects.all()
    post = Post()
    status_choices = post.get_status_choices()
    ctx = {
        'categories': categories,
        'status_choices': status_choices,
        'categories': Category.objects.all()
    }

    return render(request, 'create_post.html', ctx)


# update_post_form
@login_required
def update_post_form(request, pk):
    if request.method == 'GET':
        return __update_post_form(request, pk)
    else:
        raise Http404


@login_required
def __update_post_form(request, pk):
    categories = Category.objects.all()
    post = Post.objects.get(pk=pk)
    status_choices = post.get_status_choices()
    ctx = {
        'post': post,
        'categories': categories,
        'status_choices': status_choices,
        'categories': Category.objects.all()
    }

    return render(request, 'update_post.html', ctx)


# list
def posts_by_tag(request, tag_pk):
    if request.method == 'GET':
        per_page = 15
        page = request.GET.get('page', 1)

        target_tag = Tag.objects.get(pk=tag_pk)

        if request.user.is_authenticated():
            pg = Paginator(Post.objects.filter(tags__in=[target_tag]), per_page)
        else:
            pg = Paginator(Post.objects.filter(status='public', tags__in=[target_tag]), per_page)

        return __render_index(request, pg, page)
    else:
        raise Http404


def posts_by_category(request, category_pk):
    if request.method == 'GET':
        per_page = 15
        page = request.GET.get('page', 1)

        target_category = Category.objects.get(pk=category_pk)

        if request.user.is_authenticated():
            pg = Paginator(Post.objects.filter(category=target_category), per_page)
        else:
            pg = Paginator(Post.objects.filter(status='public', category=target_category), per_page)

        return __render_index(request, pg, page)
    else:
        raise Http404


def __render_index(request, pg, page):
    try:
        contents = pg.page(page)
    except PageNotAnInteger:
        contents = pg.page(1)
    except EmptyPage:
        contents = []

    ctx = {
        'posts': contents,
        'categories': Category.objects.all()
    }

    return render(request, 'index.html', ctx)