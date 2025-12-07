from rest_framework.permissions import BasePermission



# ====================================================================
# can view group permissions
# ====================================================================
class CanViewGroup(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("auth.view_group") 
# ====================================================================
# 
# 
# 
# ====================================================================
# can create group permissions
# ====================================================================
class CanCreateGroup(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("auth.add_group") 
# ====================================================================
# 
# 
# 
# ====================================================================
# can update group permissions
# ====================================================================
class CanUpdateGroup(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("auth.change_group") 
# ====================================================================
# 
# 
# 
# ====================================================================
# can delete group permissions
# ====================================================================
class CanDeleteGroup(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("auth.delete_group") 
# ====================================================================