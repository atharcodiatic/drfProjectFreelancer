from django.urls import path, include
from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import  Permission
from django.contrib.contenttypes.models import ContentType
from .models import *
from .utility import *
User = get_user_model()


class JobPostSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = JobPost
        exclude = ['posted_at', 'status', 'client',]

    def create(self, validated_data):
        client = self.context['client']
        skills = validated_data.pop('skill_required')
        skill_data = [s.id for s in skills]
        job_obj = JobPost.objects.create(**validated_data, client = client)
        job_obj.skill_required.add(*skill_data)
        return job_obj
    
class JobProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        exclude = ['created_at', 'updated_at', 'freelancer', 'status']

    def create(self, validated_data):
        freelancer = self.context.get('freelancer')
        job = validated_data.get('job')
        proposal_obj = JobProposal.objects.create(**validated_data , freelancer = freelancer)
        return proposal_obj
    
class ContractSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs.get('context', {}).get('request')
        client_job = JobPost.objects.filter(client = request.user.client)\
            .values_list('id', flat=True)
        job_prop = JobProposal.objects.filter(job__id__in = client_job,
                                               status='INPROCESS')
        self.fields['proposal'].queryset = job_prop

    class Meta:
        model = Contract
        exclude= ['created_at', 'total', 'currency' , 'remaining']

    def create(self, validated_data):
        proposal_id = validated_data.get('proposal').id
        proposal_obj = JobProposal.objects.get(id = proposal_id)
        proposal_obj.status = 'ACCEPTED'
        proposal_obj.save()
        total = calculate_total(proposal_obj.job.duration, proposal_obj.job.duration_type , proposal_obj.bid)
        contract_obj = Contract.objects.create(proposal = proposal_obj, total = total, currency = proposal_obj.currency, remaining = total)
        return contract_obj


    
        