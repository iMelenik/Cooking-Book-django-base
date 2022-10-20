"""Для рендера html страниц"""

from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.shortcuts import render
from random import randint
from articles.models import Article


def home_view(request):
    """
    :param request: Django sends
    :return: HTML page
    """
    article_list = Article.objects.all()
    contex = {
        'objects_list': article_list,
    }
    HTML_STRING = render_to_string('home-view.html', context=contex)

    return HttpResponse(HTML_STRING)

