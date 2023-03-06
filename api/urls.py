from rapihogar.models import Company
from rest_framework import routers
from django.urls import path, include
from .views import CompanyViewSet, technician_list

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')


urlpatterns = [
    path('', include(router.urls)),
    path('technicians/', technician_list, name='technician_list'),

]