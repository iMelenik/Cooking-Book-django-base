from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin

from .models import Recipe, RecipeIngredient, Rating
from .forms import RecipeForm, IngredientFormset
from .validators import validate_rate

# Create your views here.
# CRUD -> Create Read Update Delete
main_menu = [
    # сделать шапку изменяемой
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Мои рецепты', 'url_name': 'recipes:user'},
    {'title': 'Создать рецепт', 'url_name': 'recipes:create'},
    {'title': 'О сайте', 'url_name': 'about'},
]


class RecipeCreateView(LoginRequiredMixin, View):
    """Создание рецепта через CBV"""
    recipe_form = RecipeForm()
    ingredients_formset = IngredientFormset(queryset=RecipeIngredient.objects.none())
    context = {
        "recipe_form": recipe_form,
        "ingredients_formset": ingredients_formset,
        "object": None,
    }

    def get(self, request):
        return render(request, 'recipes/create-edit.html', context=self.context)

    def post(self, request):
        recipe_form = RecipeForm(request.POST, request.FILES)
        ingredients_formset = IngredientFormset(request.POST, queryset=RecipeIngredient.objects.none())

        if recipe_form.is_valid() and ingredients_formset.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            for ingredient_form in ingredients_formset:
                ingredient = ingredient_form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()
            return redirect(recipe.get_absolute_url())
        return render(request, 'recipes/create-edit.html', context=self.context)


@login_required
def recipe_edit_view(request, slug=None):
    """Редактирование рецепта автором"""
    obj = get_object_or_404(Recipe, slug=slug, user=request.user)
    recipe_form = RecipeForm(request.POST or None, request.FILES or None, instance=obj)
    ingredients_formset = IngredientFormset(request.POST or None, queryset=obj.get_all_ingredients_qs())
    context = {
        "recipe_form": recipe_form,
        "ingredients_formset": ingredients_formset,
        "object": obj,
    }

    if all([recipe_form.is_valid(), ingredients_formset.is_valid()]):
        recipe = recipe_form.save()
        for ingredient_form in ingredients_formset:
            ingredient = ingredient_form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()
        return redirect(obj.get_absolute_url())
    return render(request, 'recipes/create-edit.html', context=context)


def recipe_detail_view(request, slug=None):
    """Конкретный рецепт"""
    obj = get_object_or_404(Recipe, slug=slug)
    curr_user = request.user
    is_author = obj.user == curr_user
    context = {
        "object": obj,
        "is_author": is_author,
    }

    if curr_user.is_authenticated:
        is_rated = obj.get_user_recipe_rating(curr_user)
        context["rated"]: is_rated

        if request.method == 'POST':
            try:
                rate = validate_rate(request.POST['rank'])
            except:
                context['rate_error'] = "Оценка может быть от 0 до 5."
            else:
                if is_rated:
                    # если юзер уже голосовал
                    obj.set_user_recipe_rating(rate, curr_user)
                else:
                    # если юзер не голосовал
                    Rating.objects.create(
                        recipe=obj,
                        user=curr_user,
                        rate=rate,
                    )
                    return redirect(obj.get_absolute_url())
    return render(request, 'recipes/detail.html', context)


@login_required
def user_recipes_view(request):
    """Рецепты юзера"""
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs,
        "all": False,
    }
    return render(request, 'recipes/list.html', context)


def all_recipes(request):
    """Все рецепты"""
    qs = Recipe.objects.all()
    context = {
        "object_list": qs,
        "all": True,
    }
    return render(request, 'recipes/list.html', context)


def recipe_search_view(request):
    query = request.GET.get('query', None)
    qs = None
    if query:
        qs = Recipe.objects.search(query=query)

    contex = {
        'query': query,
        'objects_list': qs,
    }
    return render(request, 'recipes/search.html', context=contex)


def recipe_delete_view(request, slug=None):
    recipe_obj = get_object_or_404(Recipe, slug=slug)
    if request.method == 'POST':
        recipe_obj.delete()
        return redirect('home')
    return render(request, "recipes/delete.html", context={})
