from django.urls import path
from .views import register_attempt,login_attempt ,succesVerification,erroVerification,compteVerified
from .views import *;
urlpatterns = [
    path('api/patients',PatientAccountViewSet.as_view({
        'get' : 'list',
        'post':'create'
    })),
    path('api/patients/<str:pk>',PatientAccountViewSet.as_view({
        'put' : 'update',
        'delete' : 'destroy'
    })),
    path('verify/<auth_token>' , verify , name="verify"),
    path('patient/login' ,login_attempt , name="login_attempt"),
    path('patient/register',register_attempt,name="register_attempt"),
    path('verify/patient/succes',succesVerification,name="succesVerification"),
    path('verify/patient/error',erroVerification,name="erroVerification"),
    path('verify/patient/compteVerif',compteVerified,name="compteVerified"),
]