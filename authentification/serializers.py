from rest_framework import serializers
from .models import PatientAccount
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class PatientAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PatientAccount
        fields = '__all__'