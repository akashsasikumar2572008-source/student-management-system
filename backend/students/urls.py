from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, DepartmentViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'departments', DepartmentViewSet, basename='department')

urlpatterns = [
    path('', include(router.urls)),
]
