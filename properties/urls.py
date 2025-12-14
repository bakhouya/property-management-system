# properties/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# app_name = 'properties'

# أنشئ Router للـ Views
router = DefaultRouter()

urlpatterns = [
    # ==========================================================================
    # مسارات أنواع الأسعار (PriceType)
    # ==========================================================================
    path('ad/price-types/', views.PriceTypeListView.as_view(), name='price-type-list'),  
    path('ad/price-types/active/', views.ActivePriceTypeListView.as_view(), name='active-price-type-list'),
   
    path('ad/price-types/<uuid:pk>/', views.PriceTypeDetailView.as_view(), name='price-type-detail'),
    path('ad/price-types/<uuid:pk>/update/', views.PriceTypeUpdateView.as_view(), name='price-type-update'),
    path('ad/price-types/<uuid:pk>/delete/', views.PriceTypeDeleteView.as_view(), name='price-type-delete'),    
    # ==========================================================================
    # مسارات العقارات (Property)
    # ==========================================================================
    path('ad/properties/', views.AdminPropertyListView.as_view(), name='property_list'), 
    path('ad/properties/<uuid:pk>/', views.AdminPropertyDetailView.as_view(), name='property_detail'),
    path('ad/properties/<uuid:pk>/delete/', views.AdminDeletePropertyDeleteView.as_view(), name='property_delete'), 
    path('ad/properties/<uuid:pk>/block/', views.AdminPropertyBlockView.as_view(), name='property_block'),

    path('ad/properties/comments/', views.AdminCommentListView.as_view(), name='comments'),
    path('ad/properties/comments/<uuid:pk>/update/', views.AdminCommentUpdateView.as_view(), name='comment_update'),
    path('ad/properties/comments/<uuid:pk>/delete/', views.AdminCommentDeleteView.as_view(), name='comment_delete'),



    path('properties/price-types/create/', views.PriceTypeCreateView.as_view(), name='price-type-create'),
    path('properties/', views.PropertyListView.as_view(), name='property-list'),   
    path('properties/create/', views.PropertyCreateView.as_view(), name='property-create'),  
    path('properties/<uuid:pk>/', views.PropertyDetailView.as_view(), name='property-detail'), 
    path('properties/<uuid:pk>/update/', views.PropertyUpdateView.as_view(), name='property-update'), 
    path('properties/<uuid:pk>/delete/', views.PropertyDeleteView.as_view(), name='property-delete'),  
    path('properties/<uuid:pk>/change-status/', views.PropertyChangeStatusView.as_view(), name='property-change-status'),   
    path('properties/<uuid:pk>/like/', views.ToggleLikeView.as_view(), name='property-like'),
    path('properties/<uuid:pk>/favorite/', views.ToggleFavoriteView.as_view(), name='property-favorite'),
    path('properties/user/<uuid:user_id>/all/', views.UserPropertyListView.as_view(), name='user-properties'),
    path('properties/user/properties/', views.MyPropertyListView.as_view(), name='my-properties'),
    path('properties/user/favorites/', views.UserFavoritesView.as_view(), name='user-favorites'),
    
    # ==========================================================================

    # ==========================================================================
    # مسارات التعليقات (Comment)
    # ==========================================================================
    path('properties/<uuid:property_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('properties/comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('properties/comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('properties/comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

]