from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentAdminViewSet,
    DepartmentCategoryAdminViewSet,
    DepartmentCategoryPublicViewSet,
    DepartmentLeaderAdminViewSet,
    DepartmentPublicViewSet,
)

router = DefaultRouter()
router.register(r'departments', DepartmentPublicViewSet, basename='departments-public')
router.register(r'department-categories', DepartmentCategoryPublicViewSet, basename='department-category-public')
router.register(r'admin/departments', DepartmentAdminViewSet, basename='departments-admin')
router.register(r'admin/department-categories', DepartmentCategoryAdminViewSet, basename='department-category-admin')
router.register(r'admin/department-leaders', DepartmentLeaderAdminViewSet, basename='department-leader-admin')

urlpatterns = router.urls
