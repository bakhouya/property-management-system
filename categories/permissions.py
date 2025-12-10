from rest_framework.permissions import BasePermission 


# ====================================================================
# can create new user                                            
# ====================================================================
class CanViewCategoryType(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.view_categorytype") 
# ====================================================================
# 
# ====================================================================
# can create new user                                           
# ====================================================================
class CanCreateCategoryType(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.add_categorytype") 
# ====================================================================
#                                  
# ====================================================================
# can create new user                                         
# ====================================================================
class CanUpdateCategoryType(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.change_categorytype") 
# ====================================================================
# 
# ====================================================================
# can create new user
# ====================================================================
class CanDeleteCategoryType(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.delete_categorytype") 
# ====================================================================




# ====================================================================
# can create new user                                            
# ====================================================================
class CanViewMainCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.view_maincategory") 
# ====================================================================
# 
# ====================================================================
# can create new user                                           
# ====================================================================
class CanCreateMainCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.add_maincategory") 
# ====================================================================
#                                  
# ====================================================================
# can create new user                                         
# ====================================================================
class CanUpdateMainCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.change_maincategory") 
# ====================================================================
# 
# ====================================================================
# can create new user
# ====================================================================
class CanDeleteMainCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.delete_maincategory") 
# ====================================================================



# ====================================================================
# can create new user                                            
# ====================================================================
class CanViewSubCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.view_subcategory") 
# ====================================================================
# 
# ====================================================================
# can create new user                                           
# ====================================================================
class CanCreateSubCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.add_subcategory") 
# ====================================================================
#                                  
# ====================================================================
# can create new user                                         
# ====================================================================
class CanUpdateSubCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.change_subcategory") 
# ====================================================================
# 
# ====================================================================
# can create new user
# ====================================================================
class CanDeleteSubCategory(BasePermission): 
    def has_permission(self, request, view):
        user = request.user 
        return user.has_perm("categories.delete_subcategory") 
# ====================================================================