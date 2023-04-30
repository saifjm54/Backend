from django.shortcuts import render,redirect
from rest_framework import viewsets,status
from .models import PatientAccount,PraticienAccount
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import PatientAccountSerializer,UserSerializer
from django.core.mail import send_mail
import uuid
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view,renderer_classes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
import json
from django.urls import reverse
# Create your views here.
def register_attempt(request):
        if request.method == 'POST':
            url = reverse('')
        return render(request, 'patient/register.html')

@login_required
@renderer_classes((TemplateHTMLRenderer,))
def home(request):
    return render(request , 'home.html')

def send_mail_after_registration(email,token):
    subject = 'You Accounnt need to be verified '
    message = f'Hi paste the link to verify you account http://127.0.0.1:8000/auth/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer,))
def verify(request,auth_token):
    try:
        patient = PatientAccount.objects.get(auth_token=auth_token)
        if patient:
            if patient.user.is_active:
                return redirect('patient/compteVerif')
            user=patient.user
            user.is_active = True
            user.save()
            patient.save()
            return redirect('patient/succes')
        else : 
            return redirect('patient/error')
    except Exception as e :
        print(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,template_name='error.html')


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def succesVerification(request):
    data = {
                'message':'Your account has been verified.'
            }
    return Response(data,template_name='success.html')
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def erroVerification(request):
    data = {
                'message' : 'Profile does not exist'
            }
    return Response(data,template_name='error.html')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def compteVerified(request):
    data = {
                'message':'Your account has been verified.'
            }
    return Response(data,template_name='success.html')


@renderer_classes((TemplateHTMLRenderer,))
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username = username)
        if user is None:
            data={
            'message' : 'User not found.'
                  } 
            return Response(data,status=status.HTTP_404_NOT_FOUND,template_name='patient/login.html')
        patient = PatientAccount.objects.get(user=user)
        if not patient.user.is_active:
            data = {
                'message':'Profile is not verified check your mail.'
                        }
            return Response(data=data,template_name='patient/login.html',status=status.HTTP_405_METHOD_NOT_ALLOWED)
            user = authenticate(username=username,password=password)
            if user is None:
                data = {
                'message':'Wrong password.'
                    }
                return Response(data=data,status=status.HTTP_403_FORBIDDEN,template_name='patient/login.html')
            login(request, user)
            return Response(template_name='home.html',status=status.HTTP_200_OK)
        return render(request, 'patient/login.html')

class PatientAccountViewSet(viewsets.ViewSet):

    @permission_classes([IsAuthenticated])
    def list(self,request):
        patients = PatientAccount.objects.all()
        serializer = PatientAccountSerializer(patients,many=True)
        return Response(serializer.data)
    
    #@api_view(('POST',))
    @renderer_classes((TemplateHTMLRenderer,))
    def create(self,request):
        data = request.data 
        username = data['username']
        email = data['email']
        password = data['password']
        try:
            # Check Username exists ?
            if User.objects.filter(username=username).exists():
                data = {
                    'username' : 'user with this username already exists'
                }
                return Response(data=data,status=status.HTTP_406_NOT_ACCEPTABLE)
            if User.objects.filter(email=email).exists():
                data = {
                    'email' : 'user with this email already exists'
                }
                return Response(data=data,status=status.HTTP_406_NOT_ACCEPTABLE)
            # Create User 
            user = User(username=username,first_name=data['firstname'],last_name=data['lastname'],email=data['email'])
            user.set_password(password)
            user.is_active = False
            user.save()
            # Create PatientAccount
            auth_token = str(uuid.uuid4())
            patient = PatientAccount.objects.create(user=user,auth_token=auth_token,tel=data['telephone'],birthday=data['birthday'])
            patient.save()
            send_mail_after_registration(email , auth_token)
            data = {
                'message' : ['We have sent an email to you ','Please check your mail']
            }
            return Response(data,status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            
        return Response(status=status.HTTP_400_BAD_REQUEST,template_name='error.html')
    #@api_view(('PUT',))
    @renderer_classes((TemplateHTMLRenderer,))
    def update(self,request,pk):
        patient = PatientAccount.objects.get(id=pk)
        user = patient.user
        data = request.data
        serializer = UserSerializer(instance=user,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if patient['tele'] != data['telephone']:
            patient['tel'] = data['telephone']
            patient.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED,template_name='success.html')
    
   # @api_view(('DELETE',))
    @renderer_classes((TemplateHTMLRenderer,))
    def destroy(self,request,pk=None):
        patient = PatientAccount.objects.get(id = pk)
        if patient is not None:
            patient.user.delete()
            patient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT,template_name='success.html')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,template_name='error.html')
        

class PraticienAccountViewSet(viewsets.ViewSet):
    @login_required
    @renderer_classes((TemplateHTMLRenderer,))
    def home(request):
        return render(request , 'home.html')
    
    @api_view(('POST',))
    @renderer_classes((TemplateHTMLRenderer,))
    def login_attempt(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username).first()
        if user is None:
            data={
                'message' : 'User not found.'
            }
            return Response(data,status=status.HTTP_404_NOT_FOUND,template_name='login.html')
        praticien = PraticienAccount.objects.filter(user=user).first()

        if not patient.user.is_active:
            data = {
                'message':'Profile is not verified check your mail.'
            }
            return Response(data=data,template_name='login.html',status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = authenticate(username=username,password=password)
        if user is None:
            data = {
                'message':'Wrong password.'
            }
            return Response(data=data,status=status.HTTP_403_FORBIDDEN,template_name='login.html')
        login(request, user)
        return Response(template_name='home.html',status=status.HTTP_200_OK)