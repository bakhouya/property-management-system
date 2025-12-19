
from django.urls import path
from . import views

urlpatterns = [
    # ==========================================================================
    # urls price type 
    # ==========================================================================
    path('ad/price-types/', views.PriceTypeListView.as_view(), name='price_types'),  
    path('ad/price-types/active/', views.ActivePriceTypeListView.as_view(), name='active_price_types'),  
    path('ad/price-types/create/', views.PriceTypeUpdateView.as_view(), name='create_price_type'),
    path('ad/price-types/<uuid:pk>/', views.PriceTypeDetailView.as_view(), name='price_type'),
    path('ad/price-types/<uuid:pk>/update/', views.PriceTypeUpdateView.as_view(), name='price_type_update'),
    path('ad/price-types/<uuid:pk>/delete/', views.PriceTypeDeleteView.as_view(), name='price_type_delete'),   


    # ==========================================================================
    # Urls properties & comment for admin panel
    # ==========================================================================
    # properties
    path('ad/properties/', views.AdminPropertyListView.as_view(), name='properties'), 
    path('ad/properties/<uuid:pk>/', views.AdminPropertyDetailView.as_view(), name='property'),
    path('ad/properties/<uuid:pk>/delete/', views.AdminDeletePropertyDeleteView.as_view(), name='property_delete'), 
    path('ad/properties/<uuid:pk>/block/', views.AdminPropertyBlockView.as_view(), name='property_block'),
    # comments
    path('ad/properties/comments/', views.AdminCommentListView.as_view(), name='comments'),
    path('ad/properties/comments/<uuid:pk>/update/', views.AdminCommentUpdateView.as_view(), name='comment_update'),
    path('ad/properties/comments/<uuid:pk>/delete/', views.AdminCommentDeleteView.as_view(), name='comment_delete'),

    # ==========================================================================
    # Urls properties & comment for clients
    # ==========================================================================
    path('properties/', views.PropertyListView.as_view(), name='properties'),   
    path('properties/create/', views.PropertyCreateView.as_view(), name='property_create'),  
    path('properties/<uuid:pk>/', views.PropertyDetailView.as_view(), name='property_detail'), 
    path('properties/<uuid:pk>/update/', views.PropertyUpdateView.as_view(), name='property_update'), 
    path('properties/<uuid:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),  
    path('properties/<uuid:pk>/change-status/', views.PropertyChangeStatusView.as_view(), name='property_change_status'),   
    path('properties/<uuid:pk>/like/', views.ToggleLikeView.as_view(), name='property_like'),
    path('properties/<uuid:pk>/favorite/', views.ToggleFavoriteView.as_view(), name='property_favorite'),
    path('properties/user/<uuid:user_id>/all/', views.UserPropertyListView.as_view(), name='user_properties'),
    path('properties/user/properties/', views.MyPropertyListView.as_view(), name='my_properties'),
    path('properties/user/favorites/', views.UserFavoritesView.as_view(), name='user-_avorites'),
    # comments
    path('properties/<uuid:property_id>/comments/', views.CommentListView.as_view(), name='comments'),
    path('properties/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('properties/comments/<uuid:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('properties/comments/<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),


]