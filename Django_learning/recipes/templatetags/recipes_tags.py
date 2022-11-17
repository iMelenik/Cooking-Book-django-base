"""Пользовательские теги шаблонов"""

from django import template
from recipes.models import Recipe


register = template.Library()


@register.simple_tag()
def get_all_recipes():
    return Recipe.objects.all()

# включающий тег (необходимо создать recipe_list.html)
# @register.inclusion_tag('recipes/recipe_list.html')
# def show_all_recipes():
#     recipes = Recipe.objects.all()
#     return {"recipes": recipes}
