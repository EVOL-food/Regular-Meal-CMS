from django.conf import settings
from modeltranslation.translator import translator, TranslationOptions
import delivery.models as models


class TitleDescriptionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = tuple(lang[0] for lang in settings.LANGUAGES)


translator.register(models.DeliveryVendor, TitleDescriptionTranslationOptions)
