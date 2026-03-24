from django.core.validators import FileExtensionValidator
from django.db import models


class Sight(models.Model):
    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    short_description_ru = models.TextField('Краткое описание (рус.)', blank=True)
    short_description_en = models.TextField('Краткое описание (англ.)', blank=True)
    short_description_kg = models.TextField('Краткое описание (кырг.)', blank=True)

    description_ru = models.TextField('Описание (рус.)', blank=True)
    description_en = models.TextField('Описание (англ.)', blank=True)
    description_kg = models.TextField('Описание (кырг.)', blank=True)

    main_image = models.ImageField(
        'Главное изображение',
        upload_to='sights/main/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )
    is_active = models.BooleanField('Активно', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-id')
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'

    def __str__(self):
        return self.title_ru


class SightImage(models.Model):
    sight = models.ForeignKey(
        Sight,
        verbose_name='Достопримечательность',
        related_name='gallery',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='sights/gallery/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )
    title_ru = models.CharField('Название (рус.)', max_length=255, blank=True)
    title_en = models.CharField('Название (англ.)', max_length=255, blank=True)
    title_kg = models.CharField('Название (кырг.)', max_length=255, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Изображение достопримечательности'
        verbose_name_plural = 'Изображения достопримечательностей'

    def __str__(self):
        return f'{self.sight_id}#{self.id}'
