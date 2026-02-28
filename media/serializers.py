from rest_framework import serializers

from backend.api_utils import absolute_file_url, localized_value
from .models import MediaCategory, MediaItem


class MediaCategoryPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = MediaCategory
        fields = ('id', 'name', 'slug', 'order')

    def get_name(self, obj):
        return localized_value(obj, 'name', self.context['lang'])


class MediaItemPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = MediaItem
        fields = ('id', 'type', 'title', 'file', 'preview_image', 'category', 'order', 'created_at')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_file(self, obj):
        return absolute_file_url(self.context['request'], obj.file)

    def get_preview_image(self, obj):
        return absolute_file_url(self.context['request'], obj.preview_image)

    def get_category(self, obj):
        return {
            'id': obj.category_id,
            'name': localized_value(obj.category, 'name', self.context['lang']),
            'slug': obj.category.slug,
        }


class MediaCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaCategory
        fields = '__all__'


class MediaItemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['file'] = absolute_file_url(request, instance.file)
            data['preview_image'] = absolute_file_url(request, instance.preview_image)
        return data
