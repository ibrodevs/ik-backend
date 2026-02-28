from rest_framework.exceptions import ValidationError

LANG_CHOICES = {'ru', 'en', 'kg'}


def get_lang_from_request(request):
    lang = request.query_params.get('lang', 'ru')
    if lang not in LANG_CHOICES:
        raise ValidationError({'lang': 'Invalid lang'})
    return lang


def localized_value(obj, field_base, lang):
    return getattr(obj, f'{field_base}_{lang}', None)


def absolute_file_url(request, file_field):
    if not file_field:
        return None
    try:
        url = file_field.url
    except ValueError:
        return None
    return request.build_absolute_uri(url)
