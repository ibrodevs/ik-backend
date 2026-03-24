from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class MediaCategory(models.Model):
    name_ru = models.CharField('Название (рус.)', max_length=255)
    name_en = models.CharField('Название (англ.)', max_length=255)
    name_kg = models.CharField('Название (кырг.)', max_length=255)
    slug = models.SlugField('Слаг', unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Категория медиа'
        verbose_name_plural = 'Категории медиа'

    def __str__(self):
        return self.name_ru


class MediaItem(models.Model):
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'
    TYPE_CHOICES = [
        (TYPE_PHOTO, 'Фото'),
        (TYPE_VIDEO, 'Видео'),
    ]

    category = models.ForeignKey(
        MediaCategory,
        verbose_name='Категория',
        related_name='items',
        on_delete=models.CASCADE,
    )
    type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)

    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    file = models.FileField(
        'Файл',
        upload_to='media/items/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'mp4'])],
    )
    preview_image = models.ImageField(
        'Превью',
        upload_to='media/previews/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order', '-created_at', '-id')
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'

    def clean(self):
        super().clean()
        if not self.file:
            return
        ext = self.file.name.lower().rsplit('.', 1)[-1] if '.' in self.file.name else ''
        image_ext = {'jpg', 'jpeg', 'png', 'webp'}
        video_ext = {'mp4'}
        if self.type == self.TYPE_PHOTO and ext not in image_ext:
            raise ValidationError({'file': 'Для типа "Фото" нужно загрузить изображение (jpg/png/webp).'})
        if self.type == self.TYPE_VIDEO and ext not in video_ext:
            raise ValidationError({'file': 'Для типа "Видео" нужно загрузить файл mp4.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title_ru
