from django.shortcuts import render, get_object_or_404, redirect
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
        article_object = form.save(commit=False)
        article_object.user = request.user
        article_object.save()
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
    except Article.DoesNotExist:
        raise Http404("Такого рецепта не существует :(")

    contex = {
        'object': article_obj,
        'user': request.user,
    }
    return render(request, "articles/details.html", context=contex)


def article_delete_view(request, slug=None):
    article_obj = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        article_obj.delete()
        return redirect('home')
    return render(request, "articles/delete.html", context={})
