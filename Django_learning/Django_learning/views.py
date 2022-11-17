"""Для рендера html страниц"""

from django.http import HttpResponse
from django.template.loader import render_to_string


def home_view(request):
    contex = {
        'user': request.user,
    }
    HTML_STRING = render_to_string('home-view.html', context=contex)

    return HttpResponse(HTML_STRING)

