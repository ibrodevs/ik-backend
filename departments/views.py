from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.api_utils import get_lang_from_request
from .models import Department, DepartmentCategory, DepartmentLeader
from .serializers import (
    DepartmentAdminSerializer,
    DepartmentCategoryAdminSerializer,
    DepartmentCategoryPublicSerializer,
    DepartmentLeaderAdminSerializer,
    DepartmentPublicSerializer,
)


class _LangMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang_from_request(self.request)
        return context


class DepartmentCategoryPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = DepartmentCategoryPublicSerializer
    queryset = DepartmentCategory.objects.filter(is_active=True).order_by('order', 'id')
    ordering_fields = ('order',)
    search_fields = ('name_ru', 'name_en', 'name_kg')


class DepartmentPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = DepartmentPublicSerializer
    ordering_fields = ('order',)
    search_fields = ('title_ru', 'title_en', 'title_kg')

    def get_queryset(self):
        qs = (
            Department.objects.filter(is_active=True, category__is_active=True)
            .select_related('category', 'leader')
            .order_by('order', 'id')
        )
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class DepartmentCategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = DepartmentCategory.objects.all().order_by('order', 'id')
    serializer_class = DepartmentCategoryAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DepartmentAdminViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('category', 'leader').all().order_by('order', 'id')
    serializer_class = DepartmentAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class DepartmentLeaderAdminViewSet(viewsets.ModelViewSet):
    queryset = DepartmentLeader.objects.select_related('department').all().order_by('id')
    serializer_class = DepartmentLeaderAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
