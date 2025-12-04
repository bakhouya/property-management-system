
from django.urls import path
from .views import (
        AdminCreateUserView, AdminUpdateUserView, UserListView, UserDeleteView, CustomLoginView, UserDetailView
    )
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    # Custom Url auth
    path('login/', CustomLoginView.as_view(), name='phone-login'),

    # default auth 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Urls User in admin panel  
    path('ad/users/', UserListView.as_view(), name='user-list'),
    path('ad/users/new/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('ad/user/<uuid:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('ad/user/<uuid:pk>/update/', AdminUpdateUserView.as_view(), name='user-update'),
    path('ad/user/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
]