from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from articles.models import Article
from .forms import ArticleForm


# Create your views here.
@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    contex = {
        'form': form
    }
    if form.is_valid():
        article_object = form.save()
        # title = form.cleaned_data.get('title')
        # content = form.cleaned_data.get('content')
        # article_object = Article.objects.create(title=title, content=content)
        contex['object'] = article_object
        contex['created'] = True
    # form = ArticleForm()
    # contex = {}
    # if request.POST:
    #     form = ArticleForm(request.POST)
    #     if form.is_valid():
    #         title = form.cleaned_data.get('title')
    #         content = form.cleaned_data.get('content')
    #         article_object = Article.objects.create(title=title, content=content)
    #         contex['object'] = article_object
    #         contex['created'] = True
    # contex['form'] = form`1
    return render(request, "articles/create.html", context=contex)


def article_search_view(request):
    try:
        query = int(request.GET['query'])
    except:
        query = None

    article_obj = Article.objects.get(id=query) if query else None
    contex = {
        'object': article_obj,
    }
    return render(request, 'articles/search.html', context=contex)


def article_detail_view(request, id=None):
    article_obj = Article.objects.get(id=id) if id else None

    contex = {
        'object': article_obj
    }

    return render(request, "articles/details.html", context=contex)
