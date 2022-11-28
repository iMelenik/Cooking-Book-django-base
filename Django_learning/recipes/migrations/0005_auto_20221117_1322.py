# Generated by Django 3.2.16 on 2022-11-17 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0004_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Время последнего редактирования'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(max_length=20, validators=[recipes.validators.validate_unit], verbose_name='Ед. измерения'),
        ),
    ]