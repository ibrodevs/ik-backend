from rest_framework import serializers

from backend.api_utils import absolute_file_url, localized_value
from .models import Department, DepartmentCategory, DepartmentLeader


class DepartmentCategoryPublicSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentCategory
        fields = ('id', 'name', 'slug', 'order')

    def get_name(self, obj):
        return localized_value(obj, 'name', self.context['lang'])


class DepartmentLeaderPublicSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = DepartmentLeader
        fields = ('full_name', 'photo', 'position', 'phone', 'email', 'address')

    def get_position(self, obj):
        return localized_value(obj, 'position', self.context['lang'])

    def get_address(self, obj):
        return localized_value(obj, 'address', self.context['lang'])

    def get_photo(self, obj):
        return absolute_file_url(self.context['request'], obj.photo)


class DepartmentPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    leader = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'icon', 'title', 'short_description', 'category', 'leader', 'order')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_short_description(self, obj):
        return localized_value(obj, 'short_description', self.context['lang'])

    def get_icon(self, obj):
        return absolute_file_url(self.context['request'], obj.icon)

    def get_category(self, obj):
        return {
            'id': obj.category_id,
            'name': localized_value(obj.category, 'name', self.context['lang']),
            'slug': obj.category.slug,
        }

    def get_leader(self, obj):
        if not hasattr(obj, 'leader'):
            return None
        return DepartmentLeaderPublicSerializer(obj.leader, context=self.context).data


class DepartmentCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentCategory
        fields = '__all__'


class DepartmentLeaderAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentLeader
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['photo'] = absolute_file_url(request, instance.photo)
        return data


class DepartmentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['icon'] = absolute_file_url(request, instance.icon)
        return data
