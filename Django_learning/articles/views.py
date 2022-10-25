from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from articles.models import Article
from .forms import ArticleForm, ArticleFormOld


# Create your views here.
@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    contex = {
        'form': form
    }
    if form.is_valid():
        article_object = form.save()
        contex['object'] = article_object
        contex['created'] = True
    return render(request, "articles/create.html", context=contex)


def article_search_view(request):
    query = request.GET.get('query', None)
    qs = None
    if query:
        qs = Article.objects.search(query=query)

    contex = {
        'query': query,
        'objects_list': qs,
    }
    return render(request, 'articles/search.html', context=contex)


def article_detail_view(request, slug=None):
    try:
        article_obj = Article.objects.get(slug=slug)
    except:
        raise Http404

    contex = {
        'object': article_obj
    }

    return render(request, "articles/details.html", context=contex)
