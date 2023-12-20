from django.urls import path, include
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import routers, serializers, viewsets
from django.shortcuts import get_object_or_404
# from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import  Permission
from django.contrib.contenttypes.models import ContentType
User = get_user_model()


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='enter password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Both password must match',
        style={'input_type': 'password', 'placeholder': 'confirm Password'}
    )
    class Meta:
        model = CustomUser
        lookup_field = 'url'
        exclude = ('date_joined', "is_superuser", "is_staff", "groups", "user_permissions",
                   "is_active", 'last_login')
        
    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError('phone number must be 10 digit')
        return value
        
    def validate(self,validated_data):
        if validated_data.get('password')!= validated_data.get('confirm_password'):
            raise serializers.ValidationError('password unmatched')
        return validated_data
        

class FreelancerSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Freelancer

    def create(self, validated_data):
        breakpoint()
        password = validated_data.pop('confirm_password')
        obj = Freelancer.objects.create(**validated_data)
        obj.set_password(password)
        content_type = ContentType.objects.get_for_model(Freelancer)
        fl_permission = Permission.objects.get(content_type=content_type , codename='is_freelancer')
        obj.user_permissions.add(fl_permission)
        obj.save()
        return obj
    
    

class ClientSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Client

    def create(self, validated_data):
        breakpoint()
        password = validated_data.pop('confirm_password')
        obj = Client.objects.create(**validated_data)
        obj.set_password(password)
        content_type = ContentType.objects.get_for_model(Client)
        cl_permission = Permission.objects.get(content_type=content_type , codename='is_client')
        obj.user_permissions.add(cl_permission)
        obj.save()
        return obj
    

class SkillSerializer(serializers.HyperlinkedModelSerializer):

    client = serializers.HiddenField(
        default= serializers.CurrentUserDefault()
    )
    class Meta:
        model = Skill
        fields = ['url', 'name', 'client']
    
    def create(self, validated_data):
        client = validated_data.pop('client')
        obj = Skill.objects.create(**validated_data, client= client.client)
        return obj

class SelfSkillSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = kwargs.get('context', {}).get('request')
        if request.method == "GET":
            if request.get_full_path_info()[-2].isdigit():
                self.fields['name'].read_only = True
                print(self.fields['name'].read_only)
            else:
                self.fields['name'].read_only = False

    freelancer = serializers.HiddenField(
        default= serializers.CurrentUserDefault()
    )
    class Meta:
        fields = ['id','freelancer', 'name', 'level']
        model = SelfSkill
        

    def create(self, validated_data):
        freelancer = validated_data.pop('freelancer').freelancer
        skill = validated_data.get('name')
        queryset = SelfSkill.objects
        if not queryset.filter(freelancer=freelancer , name=skill).exists():
            obj = queryset.create(**validated_data, freelancer=freelancer)
            obj.save()
        return obj
    
    def update(self, instance, validated_data):
        freelancer = validated_data.pop('freelancer').freelancer
        obj = get_object_or_404(SelfSkill, freelancer=freelancer.id, name=instance.name)
        obj.level = validated_data.pop('level')
        obj.save()
        return obj

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['start_date', 'end_date']


