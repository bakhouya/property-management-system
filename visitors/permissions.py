from rest_framework.permissions import BasePermission




# ====================================================================
# can view list visitors permissions
# ====================================================================
class CanViewListVisitor(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("visitors.view_list_visitor") 
# ====================================================================

# ====================================================================
# can view visitor permissions
# ====================================================================
class CanViewVisitor(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("visitors.view_visitor") 
# ====================================================================
# 
# 
# 
# ====================================================================
# can delete visitor permissions
# ====================================================================
class CanDeleteVisitor(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        if user.account_type != "admin": 
            return False 
        return user.has_perm("visitors.delete_visitor") 
# ====================================================================