from rest_framework.permissions import BasePermission

class isOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user



class isAssigned(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user

class isContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contributors.filter(id=request.user.id).exists()



