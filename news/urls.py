# news/urls.py
from news.views import HISTORYViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'history', HISTORYViewSet, basename='history')
urlpatterns = router.urls

