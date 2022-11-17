from django import forms
from django.forms.models import modelformset_factory

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'recipe-required-field'

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'picture']
        labels = {
            'name': 'Наименование рецепта',
            'description': 'Описание',
            'picture': 'Фото',
        }
        help_texts = {
            'name': 'Этот текст помогает с названием',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '3'})
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': self.required_css_class if self.fields[field].required else None,
            })


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']
        labels = {
            'name': 'Наименование ингредиента',
            'quantity': 'Количество',
            'unit': 'Ед. измерения',
        }


IngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
