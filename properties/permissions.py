from rest_framework.permissions import BasePermission






class CanViewPriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.view_pricetype')
        )

class CanCreatePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.add_pricetype')
        )

class CanUpdatePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.change_pricetype')
        )

class CanDeletePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.delete_pricetype')
        )





