
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from notifications.models import Notification
from properties.filters import PropertyFilter
from properties.permissions import CanCreatePriceType, CanDeleteComment, CanDeletePriceType, CanDeleteProperty, CanUpdateComment, CanUpdatePriceType, CanUpdateProperty, CanViewComment, CanViewPriceType, CanViewProperty, IsOwner

from .models import PriceType, Property, Comment
from .serializers import (PriceTypeSerializer, PropertyListSerializer, PropertyDetailSerializer, PropertyCreateSerializer, CommentSerializer,)
from utils.paginations import CustomDynamicPagination




# =============================================================================================================================
# A common fundamental rule for all PriceType Views
# Aimed at reducing redundancy (DRY) and standardizing the queryset and serializer
# =============================================================================================================================
class BasePriceTypeView(generics.GenericAPIView):
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer
# =============================================================================================================================
# 
# =============================================================================================================================
# General rule for displaying price list types
# Add: Pagination + Search + Ordering
# =============================================================================================================================
class BasePriceTypeListView(BasePriceTypeView):
    pagination_class = CustomDynamicPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
# =============================================================================================================================
# 
# =============================================================================================================================
# Display all price types (Administrators only, subject to permissions)
# =============================================================================================================================
class PriceTypeListView(BasePriceTypeListView, generics.ListAPIView):
    permission_classes = [CanViewPriceType]
    filterset_fields = ['status']
# =============================================================================================================================
# 
# =============================================================================================================================
# Displaying active price types is restricted to Authenticate users only
# =============================================================================================================================
class ActivePriceTypeListView(BasePriceTypeListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]    
    def get_queryset(self):
        return PriceType.objects.filter(status=True)
# =============================================================================================================================
# 
# =============================================================================================================================
# Create a new price type: Available only to those with add permissions
# =============================================================================================================================
class PriceTypeCreateView(BasePriceTypeView, generics.CreateAPIView):
    permission_classes = [CanCreatePriceType]
# =============================================================================================================================
# 
# =============================================================================================================================
# get details of a single price type
# =============================================================================================================================
class PriceTypeDetailView(BasePriceTypeView, generics.RetrieveAPIView):
    permission_classes = [CanViewPriceType]
# =============================================================================================================================
# 
# =============================================================================================================================
# Update on a price type: availble only to those with update permiisions
# =============================================================================================================================
class PriceTypeUpdateView(BasePriceTypeView, generics.UpdateAPIView):
    permission_classes = [CanUpdatePriceType]
# =============================================================================================================================
# 
# =============================================================================================================================
# Delete on a price type: availble only to those with delete permiisions
# =============================================================================================================================
class PriceTypeDeleteView(BasePriceTypeView, generics.DestroyAPIView):
    permission_classes = [CanDeletePriceType]
# =============================================================================================================================




# =============================================================================================================================
# A fundamental framework for all things real estate
# Contains a model and a standardized method for retrieving querysets
# =============================================================================================================================
class BasePropertyView:
    model = Property 
    def get_base_queryset(self):
        return self.model.objects.all()
# =============================================================================================================================
# 
# =============================================================================================================================
# General rules for displaying real estate listings
# Includes filtering, searching, sorting, and pagination
# =============================================================================================================================
class BasePropertyListView(BasePropertyView):
    serializer_class = PropertyListSerializer
    pagination_class = CustomDynamicPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']
# =============================================================================================================================
# 
# =============================================================================================================================
# Base APIView is dedicated to actions (Like, Favorite, Block...)
# =============================================================================================================================
class BasePropertyAPIView(BasePropertyView, APIView):
    pass
# =============================================================================================================================
# 
# =============================================================================================================================
# View all active and unrestricted properties: Available to all (visitors)
# =============================================================================================================================
class PropertyListView(BasePropertyListView, generics.ListAPIView):
    permission_classes = [AllowAny]
    def get_queryset(self):
        return self.get_base_queryset().filter(status=True, is_blocked=False)
# =============================================================================================================================
# 
# =============================================================================================================================
# Displaying details of a single property, Loading comments and replies to reduce the number of inquiries
# =============================================================================================================================
class PropertyDetailView(BasePropertyView, generics.RetrieveAPIView):
    serializer_class = PropertyDetailSerializer
    permission_classes = [AllowAny]   
    def get_queryset(self):
        return self.get_base_queryset().prefetch_related('comments', 'comments__replies')
    
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
# =============================================================================================================================
# 
# =============================================================================================================================
# Displaying properties of a specific user
# If it's the same user → Sees all their properties
# Otherwise → Sees only active and unrestricted properties
# =============================================================================================================================
class UserPropertyListView(BasePropertyListView, generics.ListAPIView):
    permission_classes = [AllowAny]  
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')       
        if str(self.request.user.id) == user_id:
            return self.get_base_queryset().filter(user_id=user_id)
        else:
            return self.get_base_queryset().filter(user_id=user_id,  status=True,  is_blocked=False)
# =============================================================================================================================
# 
# =============================================================================================================================
# Displaying properties only for Authenticated users
# =============================================================================================================================
class MyPropertyListView(BasePropertyListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]    
    def get_queryset(self):
        return self.get_base_queryset().filter(user=self.request.user)            
# =============================================================================================================================
# 
# =============================================================================================================================
# Displaying the user's Favorites properties
# =============================================================================================================================
class UserFavoritesView(BasePropertyListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]    
    def get_queryset(self):
        return self.request.user.property_favorites.filter(status=True, is_blocked=False)
# =============================================================================================================================
# 
# =============================================================================================================================
# Create a new property
# =============================================================================================================================
class PropertyCreateView(BasePropertyView, generics.CreateAPIView):
    serializer_class = PropertyCreateSerializer
    permission_classes = [IsAuthenticated]  
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = serializer.save(user=self.request.user)
        detail = PropertyDetailSerializer(created, context={"request": request})
        return Response(detail.data, status=status.HTTP_201_CREATED)
# =============================================================================================================================
# 
# =============================================================================================================================
# Property Update: Only property owners are allowed
# =============================================================================================================================
class PropertyUpdateView(BasePropertyView, generics.UpdateAPIView):
    serializer_class = PropertyCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]   
    def get_queryset(self):
        return self.model.objects.all()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated = self.model.objects.get(id=instance.id)
        detail = PropertyDetailSerializer(updated, context={"request": request})
        return Response(detail.data, status=status.HTTP_200_OK)
# =============================================================================================================================
# 
# =============================================================================================================================
# Property Delete: Only property owners are allowed
# =============================================================================================================================
class PropertyDeleteView(BasePropertyView, generics.DestroyAPIView):
    serializer_class = PropertyListSerializer
    permission_classes = [IsAuthenticated, IsOwner]   
    def get_queryset(self):
        return self.model.objects.all()
# =============================================================================================================================
# 
# =============================================================================================================================
# General rule for actions related to a single property
# Verify authorizations before execution
# =============================================================================================================================
class BasePropertyActionView(BasePropertyAPIView):
    permission_classes = [IsAuthenticated]    
    def get_property(self, property_id):
        property = get_object_or_404(self.model, id=property_id)
        self.check_object_permissions(self.request, property)
        return property
# =============================================================================================================================
# 
# =============================================================================================================================
# Change property status (Active / Inactive)
# =============================================================================================================================
class PropertyChangeStatusView(BasePropertyActionView):
    permission_classes = [IsAuthenticated, IsOwner]   
    def post(self, request, pk, *args, **kwargs):
        property = self.get_property(pk)
        property.change_status()
        return Response({'message': 'Change Status successfully ', 'status': property.status})
# =============================================================================================================================
# 
# =============================================================================================================================
# Base Toggle (Like / Favorite) and create notification to this action
# Used to reduce duplication
# =============================================================================================================================
class BaseToggleView(BasePropertyActionView):
    relation_field = None  
    action_name = None        
    def post(self, request, pk, *args, **kwargs):
        property = self.get_property(pk)
        user = request.user

        if getattr(property, self.relation_field).filter(id=user.id).exists():
            getattr(property, self.relation_field).remove(user)
            action_status = False
        else:
            getattr(property, self.relation_field).add(user)
            action_status = True 

            if action_status:
                Notification.objects.create_notification(
                    target_user = property.user,  
                    action_user = request.user,   
                    notification_type = self.action_name,
                    type_item = "property",
                    item_id = str(property.id),
                    item_name = property.title,
                    action= self.action_name, 
                )       
        count = getattr(property, self.relation_field).count()
        
        return Response({'action': self.action_name, 'status': action_status, 'count': count
 })
# =============================================================================================================================
# 
# =============================================================================================================================
# like 
# =============================================================================================================================
class ToggleLikeView(BaseToggleView):
    relation_field = 'likes'
    action_name = 'like'
# =============================================================================================================================
# 
# =============================================================================================================================
# Add to favorites
# =============================================================================================================================
class ToggleFavoriteView(BaseToggleView):
    relation_field = 'favorites'
    action_name = 'favorite'
# =============================================================================================================================


# =============================================================================================================================
# get all comment for property item with replies
# =============================================================================================================================
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomDynamicPagination
    
    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return Comment.objects.filter(property_id=property_id, parent__isnull=True, status=True).select_related('user').prefetch_related('replies', 'replies__user')
# =============================================================================================================================
# 
# =============================================================================================================================
# create new comment with register notification
# =============================================================================================================================
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]   
    def perform_create(self, serializer):
        property_id = self.kwargs.get('property_id')
        property = get_object_or_404(Property, id=property_id, status=True, is_blocked=False)
        serializer.save(user=self.request.user, property=property)
        Notification.objects.create_notification(
            target_user = property.user,  
            action_user = self.request.user,   
            notification_type = "comment",  
            type_item = "property",
            item_id = str(property.id),
            item_name = property.title,
            action = "commented",  
        )
# =============================================================================================================================
# 
# =============================================================================================================================
# update comment from owner 
# =============================================================================================================================
class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Comment.objects.all()

# =============================================================================================================================
# 
# =============================================================================================================================
# delete comment from owner
# =============================================================================================================================
class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def get_queryset(self):
        return Comment.objects.all()
# =============================================================================================================================




# =============================================================================================================================
# admin section: get all comments
# =============================================================================================================================
class AdminCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewComment]
    pagination_class = CustomDynamicPagination
    
    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return Comment.objects.filter(property_id=property_id, parent__isnull=True, status=True
        ).select_related('user').prefetch_related('replies', 'replies__user')
# =============================================================================================================================
# 
# =============================================================================================================================
# update comment by admin
# =============================================================================================================================
class AdminCommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanUpdateComment]
# =============================================================================================================================
# 
# =============================================================================================================================
# delete comment from admin
# =============================================================================================================================
class AdminCommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteComment]
# =============================================================================================================================
# 
# =============================================================================================================================
# get all properties for admin
# =============================================================================================================================
class AdminPropertyListView(BasePropertyListView, generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewProperty]
    def get_queryset(self):
        return self.get_base_queryset()
# =============================================================================================================================
# 
# =============================================================================================================================
# get detail property for admin
# =============================================================================================================================
class AdminPropertyDetailView(BasePropertyView, generics.RetrieveAPIView):
    serializer_class = PropertyDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewProperty]   
    def get_queryset(self):
        return self.get_base_queryset()
# =============================================================================================================================
# 
# =============================================================================================================================
# delete property for admin
# =============================================================================================================================
class AdminDeletePropertyDeleteView(BasePropertyView, generics.DestroyAPIView):
    serializer_class = PropertyListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteProperty]   
    def get_queryset(self):
        return self.model.objects.all()
# =============================================================================================================================
# 
# =============================================================================================================================
# block / unblock property for admin
# =============================================================================================================================
class AdminPropertyBlockView(BasePropertyActionView):
    permission_classes = [IsAuthenticated, IsAdminUser, CanUpdateProperty]  
    def post(self, request, pk, *args, **kwargs):
        property = self.get_property(pk)
        old_status = property.is_blocked
        property.change_blocked()
        new_status = property.is_blocked
        if old_status != new_status:

            if new_status:
                notification_type = "block"
                action_word = "blocked"
            else:
                notification_type = "unblock"
                action_word = "unblocked"
            
            Notification.objects.create_notification(
                target_user=property.user, 
                action_user=request.user,   
                notification_type=notification_type,
                type_item="property",
                item_id=str(property.id),
                item_name=property.title,
                action=action_word, 
            )
        return Response({'message': 'Chnage status blocked successfully', 'status': property.is_blocked})
# =============================================================================================================================


