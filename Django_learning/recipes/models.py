from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError
from random import randint

from .validators import validate_unit
User = settings.AUTH_USER_MODEL


# Create your models here.
class Recipe(models.Model):
    """Рецепт"""
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    picture = models.ImageField(blank=True, null=True, verbose_name='Фото')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время последнего редактирования')
    slug = models.SlugField(unique=True, max_length=50, db_index=True, null=True, blank=True)

    def __str__(self):
        return f"Рецепт {self.name}"

    def save(self, *args, **kwargs):
        """Создание слага при первичном(!) сохранении объекта"""
        if not self.slug:
            try:
                slug = slugify(translit(str(self.name), reversed=True))
            except LanguageDetectionError:
                slug = slugify(self.name)

            def slug_check(slug):
                qs = Recipe.objects.filter(slug=slug).exclude(id=self.pk)
                if qs.exists():
                    slug = f"{slug}-{self.pk + randint(1_000, 10_000)}"
                    return slug_check(slug)
                else:
                    return slug

            slug = slug_check(slug)
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse("recipes:edit", kwargs={'slug': self.slug})

    def get_all_ingredients_qs(self):
        return self.recipeingredient_set.all()

    def get_avg_recipe_rating(self):
        rate = self.rating_set.filter(recipe=self).aggregate(Avg('rate'))
        return rate['rate__avg']

    def get_user_recipe_rating(self, user):
        try:
            return self.rating_set.get(recipe=self, user=user)
        except Rating.DoesNotExist:
            return None

    def set_user_recipe_rating(self, rate, user):
        rating = self.get_user_recipe_rating(user)
        rating.rate = rate
        rating.save()

    def is_user_rated(self, user):
        try:
            self.rating_set.get(recipe=self, user=user)
            return True
        except:
            return False


class RecipeIngredient(models.Model):
    """Один из ингредиентов рецепта"""
    objects = models.Manager()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, verbose_name='Наименование')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    unit = models.CharField(max_length=20, validators=[validate_unit], verbose_name='Ед. измерения')
    # ['кг', 'г', 'ч.л', 'ст.л', 'л', 'мл', 'шт']


class Rating(models.Model):
    """Оценка рецепта юзером"""
    objects = models.Manager()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rate = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Рейтинг')
