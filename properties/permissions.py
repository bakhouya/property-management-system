from rest_framework.permissions import BasePermission



# ===============================================================================
# permissions is owner 
# ===============================================================================
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, object):
        return object.user == request.user
# ===============================================================================



# ===============================================================================
# permissions can view price type
# ===============================================================================
class CanViewPriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.view_pricetype')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can create price type
# ===============================================================================
class CanCreatePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.add_pricetype')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can update price type
# ===============================================================================
class CanUpdatePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.change_pricetype')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can delete price type
# ===============================================================================
class CanDeletePriceType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.delete_pricetype')
        )
# ===============================================================================






# ===============================================================================
# permissions can view Comment
# ===============================================================================
class CanViewComment(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.view_comment')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can update Comment
# ===============================================================================
class CanUpdateComment(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.change_comment')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can delete Comment
# ===============================================================================
class CanDeleteComment(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.delete_comment')
        )
# ===============================================================================










# ===============================================================================
# permissions can view property
# ===============================================================================
class CanViewProperty(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.view_property')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can update property
# ===============================================================================
class CanUpdateProperty(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.change_property')
        )
# ===============================================================================
# 
# ===============================================================================
# permissions can delete property
# ===============================================================================
class CanDeleteProperty(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.has_perm('properties.delete_property')
        )
# ===============================================================================
