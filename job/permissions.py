from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwnerAction(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('accounts.is_freelancer'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if obj.freelancer == request.user.freelancer:
            return True
        return False
    
class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('accounts.is_client'):
            return True
        else:
            return False
    def has_object_permission(self, request, view, obj):
        if obj.client == request.user.client:
            return True
        return False
    



        
