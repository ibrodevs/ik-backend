from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from backend.api_utils import get_lang_from_request
from .models import Employee, LeadershipMember, OfficialDocument, ProcurementItem, Project
from .serializers import (
    EmployeeAdminSerializer,
    EmployeePublicSerializer,
    LeadershipMemberAdminSerializer,
    LeadershipMemberPublicSerializer,
    OfficialDocumentAdminSerializer,
    OfficialDocumentPublicSerializer,
    ProcurementItemAdminSerializer,
    ProcurementItemPublicSerializer,
    ProjectAdminSerializer,
    ProjectPublicSerializer,
)


class _LangMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = get_lang_from_request(self.request)
        return context


class LeadershipMemberPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = LeadershipMemberPublicSerializer
    queryset = LeadershipMember.objects.filter(is_active=True).order_by('order', 'id')
    pagination_class = None
    ordering_fields = ('order',)
    search_fields = ('full_name_ru', 'full_name_en', 'full_name_kg', 'position_ru', 'position_en', 'position_kg')


class EmployeePublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = EmployeePublicSerializer
    queryset = Employee.objects.filter(is_active=True).order_by('order', 'id')
    pagination_class = None
    ordering_fields = ('order',)
    search_fields = ('full_name_ru', 'full_name_en', 'full_name_kg', 'position_ru', 'position_en', 'position_kg', 'phone', 'email')


class OfficialDocumentPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = OfficialDocumentPublicSerializer
    pagination_class = None
    ordering_fields = ('order', 'created_at')
    search_fields = ('title_ru', 'title_en', 'title_kg')

    def get_queryset(self):
        qs = OfficialDocument.objects.filter(is_active=True).order_by('order', 'id')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class ProcurementItemPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProcurementItemPublicSerializer
    pagination_class = None
    ordering_fields = ('order', 'deadline')
    search_fields = ('title_ru', 'title_en', 'title_kg', 'description_ru', 'description_en', 'description_kg')

    def get_queryset(self):
        qs = ProcurementItem.objects.filter(is_active=True).order_by('order', 'deadline', 'id')
        item_type = self.request.query_params.get('type')
        if item_type:
            qs = qs.filter(type=item_type)
        return qs


class ProjectPublicViewSet(_LangMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectPublicSerializer
    pagination_class = None
    ordering_fields = ('order',)
    search_fields = ('title_ru', 'title_en', 'title_kg', 'description_ru', 'description_en', 'description_kg')

    def get_queryset(self):
        qs = Project.objects.filter(is_active=True).order_by('order', 'id')
        project_type = self.request.query_params.get('type')
        if project_type:
            qs = qs.filter(type=project_type)
        return qs


class LeadershipMemberAdminViewSet(viewsets.ModelViewSet):
    queryset = LeadershipMember.objects.all().order_by('order', 'id')
    serializer_class = LeadershipMemberAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class EmployeeAdminViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('order', 'id')
    serializer_class = EmployeeAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class OfficialDocumentAdminViewSet(viewsets.ModelViewSet):
    queryset = OfficialDocument.objects.all().order_by('order', 'id')
    serializer_class = OfficialDocumentAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class ProcurementItemAdminViewSet(viewsets.ModelViewSet):
    queryset = ProcurementItem.objects.all().order_by('order', 'deadline', 'id')
    serializer_class = ProcurementItemAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProjectAdminViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('order', 'id')
    serializer_class = ProjectAdminSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
