
from django.conf import settings
from modeltranslation.translator import translator, TranslationOptions
import menu.models as models


class TitleTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = tuple(lang[0] for lang in settings.LANGUAGES)


class TitleDescriptionSlugTranslationOptions(TitleTranslationOptions):
    fields = ('title', 'description', 'slug')


translator.register(models.Ingredient, TitleTranslationOptions)
translator.register(models.DailyMeal, TitleTranslationOptions)
translator.register(models.Category, TitleDescriptionSlugTranslationOptions)
translator.register(models.Dish, TitleDescriptionSlugTranslationOptions)
translator.register(models.Menu, TitleDescriptionSlugTranslationOptions)