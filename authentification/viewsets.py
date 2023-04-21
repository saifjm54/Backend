from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import PatientAccount
from .serializers import PatientAccountSerializer

class PatientAccountViewSet(viewsets.ModelViewSet):
    queryset = PatientAccount.objects.all()
    serializer_class = PatientAccountSerializer

