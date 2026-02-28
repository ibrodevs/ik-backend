from rest_framework import serializers

from backend.api_utils import absolute_file_url, localized_value
from .models import News, NewsCategory


class NewsCategoryPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = NewsCategory
        fields = ('id', 'name', 'slug', 'order')

    def get_name(self, obj):
        return localized_value(obj, 'name', self.context['lang'])


class NewsPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'short_description',
            'description',
            'date',
            'category',
            'image',
            'is_hot',
            'is_main',
        )

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_short_description(self, obj):
        return localized_value(obj, 'short_description', self.context['lang'])

    def get_description(self, obj):
        return localized_value(obj, 'description', self.context['lang'])

    def get_category(self, obj):
        lang = self.context['lang']
        return {
            'id': obj.category_id,
            'name': localized_value(obj.category, 'name', lang),
        }

    def get_image(self, obj):
        return absolute_file_url(self.context['request'], obj.image)


class NewsCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = '__all__'


class NewsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['image'] = absolute_file_url(request, instance.image)
        return data
