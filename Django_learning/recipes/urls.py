from django.urls import path
from .views import *

app_name = 'recipes'
urlpatterns = [
    # path('', views.recipes_list_view, name='all'),
    # path('create/', views.RecipeCreateView.as_view(), name='create'),
    # path('<int:id>/edit/', views.recipe_edit_view, name='edit'),
    # path('<int:id>/', views.recipe_detail_view, name='detail'),
    path('', all_recipes, name='all'),
    path('my-recipes/', user_recipes_view, name='user'),
    path('create/', RecipeCreateView.as_view(), name='create'),
    path('<slug:slug>/delete', recipe_delete_view, name='delete'),
    path('<slug:slug>/edit/', recipe_edit_view, name='edit'),
    path('<slug:slug>/', recipe_detail_view, name='detail'),
    path('search', recipe_search_view, name='search'),
]
