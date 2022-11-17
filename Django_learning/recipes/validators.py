from django.core.exceptions import ValidationError

valid_recipe_ingredients_units = ['кг', 'г', 'ч.л', 'ст.л', 'л', 'мл', 'шт']


def validate_unit(value):
    """Проверка допустимых единиц измерений для ингредиента"""
    if value not in valid_recipe_ingredients_units:
        raise ValidationError(f"Допустимые единицы измерения: {', '.join(valid_recipe_ingredients_units)}")


def validate_rate(value):
    try:
        value = int(value)
    except:
        raise ValueError("Значение должно быть целым числом.")
    if not 0 <= value <= 5:
        raise ValueError("Значение должно быть от 0 до 5.")
    return int(value)
