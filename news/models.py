from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError


class NewsCategory(models.Model):
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_kg = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return self.name_ru


class News(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    short_description_ru = models.TextField(blank=True)
    short_description_en = models.TextField(blank=True)
    short_description_kg = models.TextField(blank=True)

    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_kg = models.TextField(blank=True)

    date = models.DateTimeField()
    category = models.ForeignKey(NewsCategory, related_name='news', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='news/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    is_hot = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date', '-id')
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
                raise ValidationError({'is_main': 'Only one main news item is allowed.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
