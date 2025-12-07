from rest_framework.permissions import BasePermission

# ===============================================================================
#  this file handle perimmisions settings app ===================================
# ===============================================================================


# ===============================================================================
# permissions manage settings platform 
# GET = can_view_paltformSettings
# PUT PATCH = can_chnage_paltformSettings
# ===============================================================================
class CanManagePlatformSettings(BasePermission):
    def has_permission(self, request, view):

        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_platformsettings")
        else:
            return user.has_perm("settings_app.change_platformsettings")       
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage settings social media 
# GET = can_view_socialmediasettings
# PUT PATCH = can_chnage_socialmediasettings
# ===============================================================================
class CanManageMediaSettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_socialmediasettings")
        else:
            return user.has_perm("settings_app.change_socialmediasettings") 
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage settings Seo 
# GET = can_view_seosettingss
# PUT PATCH = can_chnage_seosettings
# ===============================================================================
class CanManageSEOSettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_seosettings")
        else:
            return user.has_perm("settings_app.change_seosettings") 
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage secutity settings 
# GET = can_view_securitysettings
# PUT PATCH = can_chnage_securitysettings
# ===============================================================================
class CanManageSecuritySettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_securitysettings")
        else:
            return user.has_perm("settings_app.change_securitysettings") 
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage cities
# GET = can_view_city
# PUT PATCH = can_chnage_city
# DELETE = can_delete_city
# POST = can_add_city
# ===============================================================================
class CanManageCities(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_city")
        if request.method == "POST":
            return user.has_perm("settings_app.add_city")
        if request.method == "DELETE":
            return user.has_perm("settings_app.delete_city")
        if request.method == "PUT" or request.method == "PATCH":
            return user.has_perm("settings_app.change_city")
        else:
            return False
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage user settings use admin
# GET = can_view_usersettings
# PUT PATCH = can_change_usersettings
# ===============================================================================
class CanMangeUserSettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_usersettings")
        if request.method == "PUT" or request.method == "PATCH":
            return user.has_perm("settings_app.change_usersettings")
        else:
            return False
# ===============================================================================
# 
# 
# 
# ===============================================================================
# permissions manage user settings use admin
# GET = can_view_usersettings
# PUT PATCH = can_change_usersettings
# ===============================================================================
class CanViewUserSettings(BasePermission):
    def has_permission(self, request, view):
        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_usersettings")
        else:
            return False
# ===============================================================================