from django.core.validators import FileExtensionValidator
from django.db import models


class LeadershipMember(models.Model):
    full_name_ru = models.CharField(max_length=255)
    full_name_en = models.CharField(max_length=255)
    full_name_kg = models.CharField(max_length=255)

    position_ru = models.CharField(max_length=255)
    position_en = models.CharField(max_length=255)
    position_kg = models.CharField(max_length=255)

    photo = models.ImageField(
        upload_to='office/leadership/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководство'

    def __str__(self):
        return self.full_name_ru


class OfficialDocument(models.Model):
    CATEGORY_REGULATION = 'regulations'
    CATEGORY_ORDER = 'orders'
    CATEGORY_REPORT = 'reports'
    CATEGORY_CHOICES = [
        (CATEGORY_REGULATION, 'Regulations'),
        (CATEGORY_ORDER, 'Orders'),
        (CATEGORY_REPORT, 'Reports'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    file_ru = models.FileField(
        upload_to='office/documents/ru/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    file_en = models.FileField(
        upload_to='office/documents/en/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    file_kg = models.FileField(
        upload_to='office/documents/kg/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
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
        (TYPE_PROCUREMENT, 'State Procurement'),
        (TYPE_TENDER, 'Tender'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    description_ru = models.TextField()
    description_en = models.TextField()
    description_kg = models.TextField()

    amount_som = models.DecimalField(max_digits=14, decimal_places=2)
    deadline = models.DateField()

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
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
        (TYPE_INVESTMENT, 'Investment Project'),
        (TYPE_STATE_PROGRAM, 'State Program'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    description_ru = models.TextField()
    description_en = models.TextField()
    description_kg = models.TextField()

    implementation_period_ru = models.CharField(max_length=255)
    implementation_period_en = models.CharField(max_length=255)
    implementation_period_kg = models.CharField(max_length=255)

    image = models.ImageField(
        upload_to='office/projects/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Проект или программа'
        verbose_name_plural = 'Проекты и программы'

    def __str__(self):
        return self.title_ru
