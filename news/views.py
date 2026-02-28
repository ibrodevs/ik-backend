from rest_framework import mixins, permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.api_utils import get_lang_from_request
from .models import News, NewsCategory
from .serializers import (
    NewsAdminSerializer,
    NewsCategoryAdminSerializer,
    NewsCategoryPublicSerializer,
    NewsPublicSerializer,
)


class _LangMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang_from_request(self.request)
        return context


class NewsCategoryPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsCategoryPublicSerializer
    queryset = NewsCategory.objects.filter(is_active=True).order_by('order', 'id')
    ordering_fields = ('order',)
    search_fields = ('name_ru', 'name_en', 'name_kg')


class NewsPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = NewsPublicSerializer
    ordering_fields = ('date',)
    search_fields = ('title_ru', 'title_en', 'title_kg')

    def get_queryset(self):
        qs = (
            News.objects.filter(is_active=True, category__is_active=True)
            .select_related('category')
            .order_by('-date', '-id')
        )
        category_id = self.request.query_params.get('category_id')
        if category_id:
            qs = qs.filter(category_id=category_id)
        is_hot = self.request.query_params.get('is_hot')
        if is_hot is not None:
            qs = qs.filter(is_hot=is_hot.lower() == 'true')
        is_main = self.request.query_params.get('is_main')
        if is_main is not None:
            qs = qs.filter(is_main=is_main.lower() == 'true')
        return qs


class NewsCategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = NewsCategory.objects.all().order_by('order', 'id')
    serializer_class = NewsCategoryAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NewsAdminViewSet(viewsets.ModelViewSet):
    queryset = News.objects.select_related('category').all().order_by('-date', '-id')
    serializer_class = NewsAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
