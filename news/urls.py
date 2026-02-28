from rest_framework.routers import DefaultRouter

from .views import (
    NewsAdminViewSet,
    NewsCategoryAdminViewSet,
    NewsCategoryPublicViewSet,
    NewsPublicViewSet,
)

router = DefaultRouter()
router.register(r'news', NewsPublicViewSet, basename='news-public')
router.register(r'news-categories', NewsCategoryPublicViewSet, basename='news-category-public')
router.register(r'admin/news', NewsAdminViewSet, basename='news-admin')
router.register(r'admin/news-categories', NewsCategoryAdminViewSet, basename='news-category-admin')

urlpatterns = router.urls
