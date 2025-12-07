
from rest_framework.permissions import BasePermission 


# ====================================================================
# can create new user
# ====================================================================
class CanAddUser(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.add_user") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can view detail user
# ====================================================================
class CanViewUser(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin":  
            return False 
        return user.has_perm("accounts.view_user") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can update user
# ====================================================================
class CanChangeUser(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.change_user")
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can delete user
# ====================================================================
class CanDeleteUser(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.delete_user") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can activate user
# ====================================================================
class CanActivateUser(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.can_activate_user") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can blocked user
# ====================================================================  
class CanBlockUser(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.can_block_user")
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can view list users
# ====================================================================
class CanListUsers(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.can_list_users") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
#  can veiw profile user
# ====================================================================
class CanViewUserProfile(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.can_view_user_profile") 
# ====================================================================
# 
# 
# 
# 
# ====================================================================
# can edit profile user
# ====================================================================
class CanEditUserProfile(BasePermission): 
    def has_permission(self, request, view): 
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("accounts.can_edit_user_profile")
# ====================================================================

