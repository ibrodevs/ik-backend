from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.api_utils import get_lang_from_request
from .models import MediaCategory, MediaItem
from .serializers import (
    MediaCategoryAdminSerializer,
    MediaCategoryPublicSerializer,
    MediaItemAdminSerializer,
    MediaItemPublicSerializer,
)


class _LangMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang_from_request(self.request)
        return context


class MediaCategoryPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MediaCategoryPublicSerializer
    queryset = MediaCategory.objects.filter(is_active=True).order_by('order', 'id')
    ordering_fields = ('order',)
    search_fields = ('name_ru', 'name_en', 'name_kg')


class MediaItemPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MediaItemPublicSerializer
    ordering_fields = ('order', 'created_at')
    search_fields = ('title_ru', 'title_en', 'title_kg')

    def get_queryset(self):
        qs = (
            MediaItem.objects.filter(is_active=True, category__is_active=True)
            .select_related('category')
            .order_by('order', '-created_at', '-id')
        )
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        item_type = self.request.query_params.get('type')
        if item_type:
            qs = qs.filter(type=item_type)
        return qs


class MediaCategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = MediaCategory.objects.all().order_by('order', 'id')
    serializer_class = MediaCategoryAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MediaItemAdminViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.select_related('category').all().order_by('order', '-created_at', '-id')
    serializer_class = MediaItemAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
