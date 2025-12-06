from django.urls import path
from .views import  (
    PermissionListView,
    GroupListView,
    GroupDetailView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView
)

urlpatterns = [
    path('ad/permissions/', PermissionListView.as_view(), name='permissions'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:id>/', GroupDetailView.as_view(), name='group-detail'),
    path('groups/<int:id>/update/', GroupUpdateView.as_view(), name='group-update'),
    path('groups/<int:id>/delete/', GroupDeleteView.as_view(), name='group-delete'),
]
