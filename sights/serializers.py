from rest_framework import serializers

from backend.api_utils import absolute_file_url, localized_value
from .models import Sight, SightImage


class SightImagePublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = SightImage
        fields = ('id', 'title', 'image', 'order')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_image(self, obj):
        return absolute_file_url(self.context['request'], obj.image)


class SightPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()

    class Meta:
        model = Sight
        fields = (
            'id',
            'title',
            'short_description',
            'description',
            'main_image',
            'gallery',
        )

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_short_description(self, obj):
        return localized_value(obj, 'short_description', self.context['lang'])

    def get_description(self, obj):
        return localized_value(obj, 'description', self.context['lang'])

    def get_main_image(self, obj):
        return absolute_file_url(self.context['request'], obj.main_image)

    def get_gallery(self, obj):
        serializer = SightImagePublicSerializer(
            obj.gallery.all().order_by('order', 'id'),
            many=True,
            context=self.context,
        )
        return serializer.data


class SightAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sight
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['main_image'] = absolute_file_url(request, instance.main_image)
        return data


class SightImageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightImage
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['image'] = absolute_file_url(request, instance.image)
        return data
