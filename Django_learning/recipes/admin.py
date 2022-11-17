from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
from .models import Recipe, RecipeIngredient, Rating


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'name', 'user', 'timestamp', 'updated']
    list_display_links = ['name']
    search_fields = ['name']
    readonly_fields = ['slug', 'timestamp', 'updated']
    raw_id_fields = ['user']

    class RecipeIngredientInline(admin.TabularInline):
        model = RecipeIngredient
        extra = 1

    class RatingInLine(admin.TabularInline):
        model = Rating
        extra = 0

    inlines = [RecipeIngredientInline, RatingInLine]


admin.site.register(Recipe, RecipeAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipe_name', 'quantity', 'unit']
    list_display_links = ['name']
    search_fields = ['name']

    @staticmethod
    def recipe_name(obj):
        return obj.recipe.name


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'user', 'rate']
    list_display_links = ['recipe']
    search_fields = ['recipe', 'user']
    ordering = ['recipe']


admin.site.register(Rating, RatingAdmin)
