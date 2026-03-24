from django.core.validators import FileExtensionValidator
from django.db import models


class DepartmentCategory(models.Model):
    name_ru = models.CharField('Название (рус.)', max_length=255)
    name_en = models.CharField('Название (англ.)', max_length=255)
    name_kg = models.CharField('Название (кырг.)', max_length=255)
    slug = models.SlugField('Слаг', unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Категория подразделения'
        verbose_name_plural = 'Категории подразделений'

    def __str__(self):
        return self.name_ru


class Department(models.Model):
    icon = models.FileField(
        'Иконка',
        upload_to='departments/icons/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'svg'])],
    )
    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    short_description_ru = models.TextField('Краткое описание (рус.)', blank=True)
    short_description_en = models.TextField('Краткое описание (англ.)', blank=True)
    short_description_kg = models.TextField('Краткое описание (кырг.)', blank=True)

    category = models.ForeignKey(
        DepartmentCategory,
        verbose_name='Категория',
        related_name='departments',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField('Активно', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return self.title_ru


class DepartmentLeader(models.Model):
    department = models.OneToOneField(
        Department,
        verbose_name='Подразделение',
        related_name='leader',
        on_delete=models.CASCADE,
    )
    full_name = models.CharField('ФИО', max_length=255)
    photo = models.ImageField(
        'Фотография',
        upload_to='departments/leaders/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    position_ru = models.CharField('Должность (рус.)', max_length=255)
    position_en = models.CharField('Должность (англ.)', max_length=255)
    position_kg = models.CharField('Должность (кырг.)', max_length=255)

    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)

    address_ru = models.CharField('Адрес (рус.)', max_length=255, blank=True)
    address_en = models.CharField('Адрес (англ.)', max_length=255, blank=True)
    address_kg = models.CharField('Адрес (кырг.)', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Руководитель подразделения'
        verbose_name_plural = 'Руководители подразделений'

    def __str__(self):
        return self.full_name
