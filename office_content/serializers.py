from rest_framework import serializers

from backend.api_utils import absolute_file_url, localized_value
from .models import Employee, LeadershipMember, OfficialDocument, ProcurementItem, Project


def localized_file(obj, field_base, lang):
    return getattr(obj, f'{field_base}_{lang}', None)


class LeadershipMemberPublicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = LeadershipMember
        fields = ('id', 'full_name', 'position', 'photo', 'order')

    def get_full_name(self, obj):
        return localized_value(obj, 'full_name', self.context['lang'])

    def get_position(self, obj):
        return localized_value(obj, 'position', self.context['lang'])

    def get_photo(self, obj):
        return absolute_file_url(self.context['request'], obj.photo)


class EmployeePublicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'position', 'phone', 'email', 'photo', 'order')

    def get_full_name(self, obj):
        return localized_value(obj, 'full_name', self.context['lang'])

    def get_position(self, obj):
        return localized_value(obj, 'position', self.context['lang'])

    def get_photo(self, obj):
        return absolute_file_url(self.context['request'], obj.photo)


class OfficialDocumentPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = OfficialDocument
        fields = ('id', 'category', 'title', 'file', 'order')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_file(self, obj):
        file_field = localized_file(obj, 'file', self.context['lang'])
        return absolute_file_url(self.context['request'], file_field)


class ProcurementItemPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = ProcurementItem
        fields = ('id', 'type', 'title', 'description', 'amount_som', 'deadline', 'order')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_description(self, obj):
        return localized_value(obj, 'description', self.context['lang'])


class ProjectPublicSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    implementation_period = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'type', 'title', 'description', 'implementation_period', 'image', 'order')

    def get_title(self, obj):
        return localized_value(obj, 'title', self.context['lang'])

    def get_description(self, obj):
        return localized_value(obj, 'description', self.context['lang'])

    def get_implementation_period(self, obj):
        return localized_value(obj, 'implementation_period', self.context['lang'])

    def get_image(self, obj):
        return absolute_file_url(self.context['request'], obj.image)


class LeadershipMemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadershipMember
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['photo'] = absolute_file_url(request, instance.photo)
        return data


class EmployeeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['photo'] = absolute_file_url(request, instance.photo)
        return data


class OfficialDocumentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialDocument
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['file_ru'] = absolute_file_url(request, instance.file_ru)
            data['file_en'] = absolute_file_url(request, instance.file_en)
            data['file_kg'] = absolute_file_url(request, instance.file_kg)
        return data


class ProcurementItemAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcurementItem
        fields = '__all__'


class ProjectAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            data['image'] = absolute_file_url(request, instance.image)
        return data
