from django.core.validators import FileExtensionValidator
from django.db import models


class LeadershipMember(models.Model):
    full_name_ru = models.CharField('ФИО (рус.)', max_length=255)
    full_name_en = models.CharField('ФИО (англ.)', max_length=255)
    full_name_kg = models.CharField('ФИО (кырг.)', max_length=255)

    position_ru = models.CharField('Должность (рус.)', max_length=255)
    position_en = models.CharField('Должность (англ.)', max_length=255)
    position_kg = models.CharField('Должность (кырг.)', max_length=255)

    photo = models.ImageField(
        'Фотография',
        upload_to='office/leadership/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководство'

    def __str__(self):
        return self.full_name_ru


class Employee(models.Model):
    full_name_ru = models.CharField('ФИО (рус.)', max_length=255)
    full_name_en = models.CharField('ФИО (англ.)', max_length=255)
    full_name_kg = models.CharField('ФИО (кырг.)', max_length=255)

    position_ru = models.CharField('Должность (рус.)', max_length=255)
    position_en = models.CharField('Должность (англ.)', max_length=255)
    position_kg = models.CharField('Должность (кырг.)', max_length=255)

    phone = models.CharField('Телефон', max_length=64)
    email = models.EmailField('Электронная почта')

    photo = models.ImageField(
        'Фотография',
        upload_to='office/employees/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name_ru


class OfficialDocument(models.Model):
    CATEGORY_REGULATION = 'regulations'
    CATEGORY_ORDER = 'orders'
    CATEGORY_REPORT = 'reports'
    CATEGORY_CHOICES = [
        (CATEGORY_REGULATION, 'Нормативные акты'),
        (CATEGORY_ORDER, 'Распоряжения'),
        (CATEGORY_REPORT, 'Отчёты'),
    ]

    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)

    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    file_ru = models.FileField(
        'PDF (рус.)',
        upload_to='office/documents/ru/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    file_en = models.FileField(
        'PDF (англ.)',
        upload_to='office/documents/en/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    file_kg = models.FileField(
        'PDF (кырг.)',
        upload_to='office/documents/kg/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Официальный документ'
        verbose_name_plural = 'Официальные документы'

    def __str__(self):
        return self.title_ru


class ProcurementItem(models.Model):
    TYPE_PROCUREMENT = 'procurement'
    TYPE_TENDER = 'tender'
    TYPE_CHOICES = [
        (TYPE_PROCUREMENT, 'Государственная закупка'),
        (TYPE_TENDER, 'Тендер'),
    ]

    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)

    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    description_ru = models.TextField('Описание (рус.)')
    description_en = models.TextField('Описание (англ.)')
    description_kg = models.TextField('Описание (кырг.)')

    amount_som = models.DecimalField('Сумма (сом)', max_digits=14, decimal_places=2)
    deadline = models.DateField('Крайний срок')

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'deadline', 'id')
        verbose_name = 'Закупка или тендер'
        verbose_name_plural = 'Закупки и тендеры'

    def __str__(self):
        return self.title_ru


class Project(models.Model):
    TYPE_INVESTMENT = 'investment'
    TYPE_STATE_PROGRAM = 'state'
    TYPE_CHOICES = [
        (TYPE_INVESTMENT, 'Инвестиционный проект'),
        (TYPE_STATE_PROGRAM, 'Государственная программа'),
    ]

    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)

    title_ru = models.CharField('Название (рус.)', max_length=255)
    title_en = models.CharField('Название (англ.)', max_length=255)
    title_kg = models.CharField('Название (кырг.)', max_length=255)

    description_ru = models.TextField('Описание (рус.)')
    description_en = models.TextField('Описание (англ.)')
    description_kg = models.TextField('Описание (кырг.)')

    implementation_period_ru = models.CharField('Период реализации (рус.)', max_length=255)
    implementation_period_en = models.CharField('Период реализации (англ.)', max_length=255)
    implementation_period_kg = models.CharField('Период реализации (кырг.)', max_length=255)

    image = models.ImageField(
        'Изображение',
        upload_to='office/projects/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Проект или программа'
        verbose_name_plural = 'Проекты и программы'

    def __str__(self):
        return self.title_ru
