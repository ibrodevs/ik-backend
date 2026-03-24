from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class NewsCategory(models.Model):
    name_ru = models.CharField('Название (рус.)', max_length=255)
    name_en = models.CharField('Название (англ.)', max_length=255)
    name_kg = models.CharField('Название (кырг.)', max_length=255)
    slug = models.SlugField('Слаг', unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Категория новости'
        verbose_name_plural = 'Категории новостей'

    def __str__(self):
        return self.name_ru


class News(models.Model):
    title_ru = models.CharField('Заголовок (рус.)', max_length=255)
    title_en = models.CharField('Заголовок (англ.)', max_length=255)
    title_kg = models.CharField('Заголовок (кырг.)', max_length=255)

    short_description_ru = models.TextField('Краткое описание (рус.)', blank=True)
    short_description_en = models.TextField('Краткое описание (англ.)', blank=True)
    short_description_kg = models.TextField('Краткое описание (кырг.)', blank=True)

    description_ru = models.TextField('Описание (рус.)', blank=True)
    description_en = models.TextField('Описание (англ.)', blank=True)
    description_kg = models.TextField('Описание (кырг.)', blank=True)

    date = models.DateTimeField('Дата публикации')
    category = models.ForeignKey(
        NewsCategory,
        verbose_name='Категория',
        related_name='news',
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='news/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    is_hot = models.BooleanField('Горячая новость', default=False)
    is_main = models.BooleanField('Главная новость', default=False)
    is_active = models.BooleanField('Активно', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date', '-id')
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        constraints = [
            models.UniqueConstraint(
                fields=['is_main'],
                condition=Q(is_main=True),
                name='unique_single_main_news_true',
            )
        ]

    def __str__(self):
        return self.title_ru

    def clean(self):
        super().clean()
        if self.is_main:
            exists = News.objects.filter(is_main=True).exclude(pk=self.pk).exists()
            if exists:
                raise ValidationError({'is_main': 'Главной может быть только одна новость.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
