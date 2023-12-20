from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsClientOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('accounts.is_freelancer'):
            if request.method in permissions.SAFE_METHODS:
                return True
        elif request.user.has_perm('accounts.is_client'):
            return True
        else:
            return False
        
class IsFreelancerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('accounts.is_client'):
            if request.method in permissions.SAFE_METHODS:
                return True
        elif request.user.has_perm('accounts.is_freelancer'):
            return True
        else:
            return False