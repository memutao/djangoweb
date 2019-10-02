import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import ArticlePostForm
from .models import ArticlePost


def article_list(request):
    tag = request.GET.get('tag')
    order = request.GET.get('order')

    article_list = ArticlePost.objects.all()

    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    if order == 'total_views':
        article_list = article_list.order_by('-total_views')


    paginator = Paginator(article_list,10)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = { 'articles': articles,
                'order': order,
                'tag': tag,}
    return render(request, 'article/list.html', context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id = id)
    article.total_views += 1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    context = {'article':article,'toc':md.toc}
    return render(request,'article/detail.html',context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            HttpResponse("ERROR")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article_post_form': article_post_form }
        return render(request,'article/create.html',context)

def article_safe_delete(request,id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id = id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("ERROR")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("ERROR")
    else:
        article_post_form = ArticlePostForm()
        context = { 'article': article, 'article_post_form': article_post_form }
        return render(request, 'article/update.html', context)