from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Recipe, RecipeIngredient


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user('qwe', password='qwe')

    def test_user_pw(self):
        checked = self.user_a.check_password('qwe')
        self.assertTrue(checked)


class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = get_user_model().objects.create_user('qwe', password='qwe')
        self.recipe_a = Recipe.objects.create(
            name='Тушеная курица',
            user=self.user_a,
            description='Тушим курицу',
        )
        self.recipe_b = Recipe.objects.create(
            name='Тушеная свинина',
            user=self.user_a,
            description='Тушим Свинину',
        )
        self.recipe_ingredient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Курица',
            quantity=1,
            unit='кг'
        )
        self.recipe_ingredient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Соль',
            quantity=2.5,
            unit='г'
        )

    def test_user_count(self):
        qs = get_user_model().objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        self.assertEqual(qs.count(), 2)

    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredients_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredients_forward_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertEqual(qs.count(), 2)

    def test_user_ingredients_f_count(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_ingredients_r_count(self):
        user = self.user_a
        ids_qs = list(user.recipe_set.all().values_list('recipeingredient', flat=True))
        qs = RecipeIngredient.objects.filter(id__in=ids_qs)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredients_unit_validation(self):
        ingredient_valid = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Тест',
            quantity=1,
            unit='г'
        )
        ingredient_valid.full_clean()

        ingredient_invalid = RecipeIngredient.objects.create(
            recipe=self.recipe_a,
            name='Тест',
            quantity=1,
            unit='фыр'
        )
        with self.assertRaises(ValidationError):
            ingredient_invalid.full_clean()


