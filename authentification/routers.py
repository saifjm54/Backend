from rest_framework import routers

from .viewsets import PatientAccountViewSet

router = routers.DefaultRouter()
router.register('api/auth/patients', PatientAccountViewSet)