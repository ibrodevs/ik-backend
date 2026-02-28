from rest_framework.routers import DefaultRouter

from .views import (
    MediaCategoryAdminViewSet,
    MediaCategoryPublicViewSet,
    MediaItemAdminViewSet,
    MediaItemPublicViewSet,
)

router = DefaultRouter()
router.register(r'media', MediaItemPublicViewSet, basename='media-public')
router.register(r'media-categories', MediaCategoryPublicViewSet, basename='media-category-public')
router.register(r'admin/media', MediaItemAdminViewSet, basename='media-admin')
router.register(r'admin/media-categories', MediaCategoryAdminViewSet, basename='media-category-admin')

urlpatterns = router.urls
