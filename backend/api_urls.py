from rest_framework.routers import DefaultRouter

from departments.views import (
    DepartmentAdminViewSet,
    DepartmentCategoryAdminViewSet,
    DepartmentCategoryPublicViewSet,
    DepartmentLeaderAdminViewSet,
    DepartmentPublicViewSet,
)
from media.views import (
    MediaCategoryAdminViewSet,
    MediaCategoryPublicViewSet,
    MediaItemAdminViewSet,
    MediaItemPublicViewSet,
)
from news.views import (
    NewsAdminViewSet,
    NewsCategoryAdminViewSet,
    NewsCategoryPublicViewSet,
    NewsPublicViewSet,
)
from office_content.views import (
    EmployeeAdminViewSet,
    EmployeePublicViewSet,
    LeadershipMemberAdminViewSet,
    LeadershipMemberPublicViewSet,
    OfficialDocumentAdminViewSet,
    OfficialDocumentPublicViewSet,
    ProcurementItemAdminViewSet,
    ProcurementItemPublicViewSet,
    ProjectAdminViewSet,
    ProjectPublicViewSet,
)
from sights.views import SightAdminViewSet, SightImageAdminViewSet, SightPublicViewSet

router = DefaultRouter()

# Public API
router.register(r'news', NewsPublicViewSet, basename='news-public')
router.register(r'news-categories', NewsCategoryPublicViewSet, basename='news-category-public')
router.register(r'sights', SightPublicViewSet, basename='sights-public')
router.register(r'departments', DepartmentPublicViewSet, basename='departments-public')
router.register(r'department-categories', DepartmentCategoryPublicViewSet, basename='department-category-public')
router.register(r'media', MediaItemPublicViewSet, basename='media-public')
router.register(r'media-categories', MediaCategoryPublicViewSet, basename='media-category-public')
router.register(r'leadership-members', LeadershipMemberPublicViewSet, basename='leadership-member-public')
router.register(r'employees', EmployeePublicViewSet, basename='employee-public')
router.register(r'documents', OfficialDocumentPublicViewSet, basename='document-public')
router.register(r'procurements', ProcurementItemPublicViewSet, basename='procurement-public')
router.register(r'projects', ProjectPublicViewSet, basename='project-public')

# Admin API
router.register(r'admin/news', NewsAdminViewSet, basename='news-admin')
router.register(r'admin/news-categories', NewsCategoryAdminViewSet, basename='news-category-admin')
router.register(r'admin/sights', SightAdminViewSet, basename='sights-admin')
router.register(r'admin/sight-images', SightImageAdminViewSet, basename='sights-image-admin')
router.register(r'admin/departments', DepartmentAdminViewSet, basename='departments-admin')
router.register(r'admin/department-categories', DepartmentCategoryAdminViewSet, basename='department-category-admin')
router.register(r'admin/department-leaders', DepartmentLeaderAdminViewSet, basename='department-leader-admin')
router.register(r'admin/media', MediaItemAdminViewSet, basename='media-admin')
router.register(r'admin/media-categories', MediaCategoryAdminViewSet, basename='media-category-admin')
router.register(r'admin/leadership-members', LeadershipMemberAdminViewSet, basename='leadership-member-admin')
router.register(r'admin/employees', EmployeeAdminViewSet, basename='employee-admin')
router.register(r'admin/documents', OfficialDocumentAdminViewSet, basename='document-admin')
router.register(r'admin/procurements', ProcurementItemAdminViewSet, basename='procurement-admin')
router.register(r'admin/projects', ProjectAdminViewSet, basename='project-admin')

urlpatterns = router.urls
