from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, VisitRequestViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'requests', VisitRequestViewSet, basename='visitrequest')

urlpatterns = [
    path('', include(router.urls)),
]
