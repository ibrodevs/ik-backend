from rest_framework.routers import DefaultRouter

from .views import SightAdminViewSet, SightImageAdminViewSet, SightPublicViewSet

router = DefaultRouter()
router.register(r'sights', SightPublicViewSet, basename='sights-public')
router.register(r'admin/sights', SightAdminViewSet, basename='sights-admin')
router.register(r'admin/sight-images', SightImageAdminViewSet, basename='sights-image-admin')

urlpatterns = router.urls
