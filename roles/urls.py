# ========================================================================================

from django.urls import path
from .views import  (
    PermissionListView, GroupListView, GroupDetailView,
    GroupCreateView, GroupUpdateView, GroupDeleteView
)
# ========================================================================================
# 
# 
# 
# 
# 
# ========================================================================================
# ========================================================================================
urlpatterns = [
    path('ad/permissions/', PermissionListView.as_view(), name='permissions'),
    path('ad/groups/', GroupListView.as_view(), name='group_list'),
    path('ad/groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('ad/groups/<int:id>/', GroupDetailView.as_view(), name='group_detail'),
    path('ad/groups/<int:id>/update/', GroupUpdateView.as_view(), name='group_update'),
    path('ad/groups/<int:id>/delete/', GroupDeleteView.as_view(), name='group_delete'),
]
# ========================================================================================

