from modeltranslation.translator import TranslationOptions, register

from . import models


@register(models.PlacePoints)
class PlacePointsTranslationOption(TranslationOptions):
    fields = [
        'description',
    ]
