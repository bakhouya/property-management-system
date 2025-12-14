
from django.urls import path
from .views import (
        AdminCreateUserView, AdminUpdateUserView, UserListView, UserDeleteView, CustomLoginView, UserDetailView,
        PersonalRegisterView, ProfileView, ToggleStatusUser
    )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)


urlpatterns = [
    # Custom Url auth Login
    path('auth/login/', CustomLoginView.as_view(), name='phone-login'),

    # default auth Login
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Urls User in admin panel  
    path('ad/users/', UserListView.as_view(), name='user-list'),
    path('ad/user/new/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('ad/user/<uuid:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('ad/user/<uuid:pk>/update/', AdminUpdateUserView.as_view(), name='user-update'),
    path('ad/user/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('ad/user/<uuid:pk>/change-status/', ToggleStatusUser.as_view(), name='smart-toggle'),

    path('accounts/register/', PersonalRegisterView.as_view(), name='register'),
    path('accounts/profile/', ProfileView.as_view(), name='register'),

]