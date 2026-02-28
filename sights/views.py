from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.api_utils import get_lang_from_request
from .models import Sight, SightImage
from .serializers import (
    SightAdminSerializer,
    SightImageAdminSerializer,
    SightPublicSerializer,
)


class _LangMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang_from_request(self.request)
        return context


class SightPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = SightPublicSerializer
    queryset = Sight.objects.filter(is_active=True).prefetch_related('gallery').order_by('-created_at', '-id')
    search_fields = ('title_ru', 'title_en', 'title_kg')


class SightAdminViewSet(viewsets.ModelViewSet):
    queryset = Sight.objects.all().prefetch_related('gallery').order_by('-created_at', '-id')
    serializer_class = SightAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class SightImageAdminViewSet(viewsets.ModelViewSet):
    queryset = SightImage.objects.select_related('sight').all().order_by('order', 'id')
    serializer_class = SightImageAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
