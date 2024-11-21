from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JudgmentViewSet

router = DefaultRouter()
router.register(r'l1', JudgmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
