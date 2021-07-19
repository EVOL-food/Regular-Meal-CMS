from modeltranslation.translator import TranslationOptions


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

    required_languages = ('en', 'ru')


class DishTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')

    required_languages = ('en', 'ru')


class DailyMealTranslationOptions(TranslationOptions):
    fields = ('title',)

    required_languages = ('en', 'ru')
