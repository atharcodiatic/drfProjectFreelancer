from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.generics import RetrieveUpdateAPIView,\
      GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from .models import *
from .serializers import * 
from rest_framework import status
from rest_framework.response import Response
from accounts.permissions import *
from .permissions import *

class JobPostViewSet(GenericAPIView):
    queryset = JobPost.objects
    serializer_class = JobPostSerializer
    permission_classes = [IsClientOrReadOnly]

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['client'] = self.request.user.client
        return context

    def get(self, request, format=None):
        qs = ''
        perm_obj = request.user.has_perm
        if perm_obj('accounts.is_client'):
            qs = JobPost.objects.filter(client = request.user.id)
        elif perm_obj('accounts.is_freelancer'):
            qs = JobPost.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context = self.get_serializer_context())
        if serializer.is_valid():
            serializer.save()
            return Response('ok', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobPostEditViewSet(RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsClientUser]

    def update(self, request, *args, **kwargs):
        if self.queryset.filter(id = kwargs['pk']).first().status == "OPEN":
            return super().update(request, *args, **kwargs)
        else:
            return Response('job closed', status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        if self.queryset.filter(id = kwargs['pk']).first().status == "OPEN":
            return self.destroy(request, *args, **kwargs)
        else:
            return Response('status closed', status=status.HTTP_404_NOT_FOUND)
        
class JobProposalViewset(ListCreateAPIView):
    '''
    freealncer can fetch his own proposals and create a proposal
    '''
    queryset = JobProposal.objects.all()
    serializer_class = JobProposalSerializer
    permission_classes = [IsFreelancerOrReadOnly]

    def filter_queryset(self, queryset):
        query = self.request.query_params
        if query:
            job_id = query.get('job')
            queryset = queryset.filter(job = job_id)
        else:
            queryset = queryset.filter(freelancer = self.request.user.id)
        return super().filter_queryset(queryset)

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        if self.request.user.has_perm('accounts.is_freelancer'):
            context['freelancer'] = self.request.user.freelancer
        return context
    
    def post(self, request, *args, **kwargs):
        if not JobProposal.objects.filter(freelancer = self.request.user.freelancer, job = request.data.get('job')).exists():
            return self.create(request, *args, **kwargs)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
class JobProposalEditView(RetrieveUpdateDestroyAPIView):
    queryset = JobProposal.objects.all()
    serializer_class = JobProposalSerializer
    permission_classes = [IsOwnerAction]

    def update(self, request, *args, **kwargs):
        setattr(self, 'pk_', kwargs['pk'])
        if not self.queryset.filter(id = self.pk_).first().status == "ACCEPTED":
            return super().update(request, *args, **kwargs)
        else:
            return Response('job closed', status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        if not self.queryset.filter(id = self.pk_).first().status == "ACCEPTED":
            return self.destroy(request, *args, **kwargs)
        else:
            return Response('status closed', status=status.HTTP_404_NOT_FOUND)
        
class ContractView(ListCreateAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsClientUser]
    http_method_names = ['get', 'post', 'head']

    def filter_queryset(self, queryset):
        client_job = JobPost.objects.filter(client = self.request.user.client)\
            .values_list('id', flat=True)
        job_prop = JobProposal.objects.filter(job__id__in = client_job,
                                               status='ACCEPTED')
        queryset = queryset.filter(proposal__id__in = job_prop)
        return super().filter_queryset(queryset)
    
        
    
    


    
    


    


    



    
    
    




            

    
    
