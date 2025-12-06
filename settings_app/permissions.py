from rest_framework.permissions import BasePermission




class CanManagePlatformSettings(BasePermission):
    def has_permission(self, request, view):

        user = request.user 
        if request.method == "GET":
            return user.has_perm("settings_app.view_platformsettings")
        else:
            return user.has_perm("settings_app.change_platformsettings")       


class CanViewMediaSettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.view_socialmediasettings")


class CanChangeMediaSettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.change_socialmediasettings")


class CanViewSEOSettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.view_seosettings")


class CanChangeSEOSettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.change_seosettings")


class CanViewSecuritySettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.view_securitysettings")


class CanChangeSecuritySettings(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.change_securitysettings")


class CanManageCities(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("settings_app.view_city")
    
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            return request.user.has_perm("settings_app.change_city")
        return True
