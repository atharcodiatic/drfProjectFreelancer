from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView,\
    ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from job.permissions import *
from django.contrib.auth.models import  Permission
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication or JWTAuthentication]
    permissions_classes = [IsAuthenticated]

class FreelancerViewSet(viewsets.ModelViewSet):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = ['username', 'first_name','selfskill__name']
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        perm_obj = self.request.user.has_perm
        if perm_obj('accounts.is_client'):
            return self.queryset
        elif perm_obj('accounts.is_freelancer'):
            return self.queryset.objects.filter(freelancer = self.request.user)


class ClientSignup(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class FreelancerSignup(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = FreelancerSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permissions_classes = [IsAuthenticated]

class SelfSkillViewSet(viewsets.ModelViewSet): 
    serializer_class = SelfSkillSerializer
    queryset = SelfSkill.objects.all()
    permission_classes = [IsOwnerAction]

    def get_queryset(self):
        return self.queryset.filter(freelancer = self.request.user.id)
        
 
class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.filter(client=None)
    serializer_class = SkillSerializer
    http_method_names = ['get', 'post', 'head']
    permission_classes = [IsClientOrReadOnly]



    


