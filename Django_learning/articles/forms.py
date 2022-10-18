from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        title = self.cleaned_data.get('title')
        qs = Article.objects.filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', 'Уже имеется рецепт с данным названием')

        return self.cleaned_data


class ArticleFormOld(forms.Form):
    title = forms.CharField(min_length=3, max_length=25)
    content = forms.CharField(min_length=1, max_length=1000)

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if title == '123':
    #         raise forms.ValidationError("Название 123 не приемлемо.")
    #     return title

    def clean(self):
        if self.cleaned_data.get('title') == '123':
            self.add_error('title', "Название 123 не приемлемо.")
            # raise forms.ValidationError("Общая ошибка")

        if '123' in self.cleaned_data.get('content'):
            self.add_error('content', '123 недопустимо в тексте')
            # raise forms.ValidationError("Общая ошибка")

        return self.cleaned_data
