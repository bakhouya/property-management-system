
# ===========================================================================================================
# ===========================================================================================================
from rest_framework import generics, status , filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from categories.permissions import (
    CanCreateCategoryType, CanDeleteCategoryType, CanUpdateCategoryType, CanViewCategoryType,
    CanCreateMainCategory, CanDeleteMainCategory, CanUpdateMainCategory, CanViewMainCategory,
    CanCreateSubCategory, CanDeleteSubCategory, CanUpdateSubCategory, CanViewSubCategory,
)
from utils.paginations import CustomDynamicPagination
from .models import CategoryType, MainCategory, SubCategory
from .serializers import (
    CategoryTypeSerializer, MainCategorySerializer, SubCategorySerializer, MainCategoryWithSubsSerializer, CategoryTypeWithSubsSerializer)
# ===========================================================================================================





# ===========================================================================================================
# BaseAdminListView:
# - Generic reusable list view for Admin Panel
# - Provides: search, filters, ordering, pagination, caching
# - All admin list endpoints extend this view to avoid duplication
# ===========================================================================================================
class BaseAdminListView(generics.ListAPIView):
    model                = None
    serializer_class     = None
    permission_classes   = [IsAuthenticated, IsAdminUser]
    pagination_class     = CustomDynamicPagination
    # active filter & search & ordering
    filter_backends      = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields        = ["title", "description"]
    filterset_fields     = ["title", "description", "status"]
    ordering_fields      = ["title", "created_at"]
   
    def get_queryset(self):
        return self.model.objects.all()
    
    @method_decorator(cache_page(60 * 5)) 
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin list of Category Types (requires view_categorytype permission)
# ===========================================================================================================
class AdminCategoryTypeListView(BaseAdminListView):
    model               = CategoryType
    serializer_class    = CategoryTypeSerializer
    permission_classes  = [CanViewCategoryType]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin list of main categories (requires view_maincategory permission)
# ===========================================================================================================
class AdminMainCategoryListView(BaseAdminListView):
    model               = MainCategory
    serializer_class    = MainCategorySerializer
    permission_classes  = [CanViewMainCategory]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin list of sub categories (requires view_subcategory permission)
# ===========================================================================================================
class AdminSubCategoryListView(BaseAdminListView):
    model               = SubCategory
    serializer_class    = SubCategorySerializer
    filterset_fields    = ["main", "types"]
    permission_classes  = [CanViewSubCategory]
# ===========================================================================================================




# ===========================================================================================================
# BaseAdminDetailView: generic detail view for admin resources
# ===========================================================================================================
class BaseAdminDetailView(generics.RetrieveAPIView):
    model = None
    serializer_class = None
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get_queryset(self):
        return self.model.objects.all()
# ===========================================================================================================
# 
# ===========================================================================================================
# ===========================================================================================================
# Admin get item of categorytype (requires view_categorytype permission)
# ===========================================================================================================
class AdminCategoryTypeDetailView(BaseAdminDetailView):
    model = CategoryType
    serializer_class = CategoryTypeWithSubsSerializer
    permission_classes = [CanViewCategoryType]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin get item of main categories (requires view_maincategory permission)
# ===========================================================================================================
class AdminMainCategoryDetailView(BaseAdminDetailView):
    model = MainCategory
    serializer_class = MainCategoryWithSubsSerializer
    permission_classes = [CanViewMainCategory]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin get item of sub categories (requires view_subcategory permission)
# ===========================================================================================================
class AdminSubCategoryDetailView(BaseAdminDetailView):
    model = SubCategory
    serializer_class = SubCategorySerializer
    permission_classes = [CanViewSubCategory]
# ===========================================================================================================




# ===========================================================================================================
# BaseAdminDeleteView: generic delete view (requires delete_* permission) 
# ===========================================================================================================
class BaseAdminDeleteView(generics.DestroyAPIView):
    model = None
    serializer_class = None
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return self.model.objects.all()
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin delete item  category type (requires delete_categorytype permission)
# ===========================================================================================================
class AdminCategoryTypeDeleteView(BaseAdminDeleteView):
    model = CategoryType
    serializer_class = CategoryTypeSerializer
    permission_classes = [CanDeleteCategoryType]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin delete item  main categories (requires delete_maincategory permission)
# ===========================================================================================================
class AdminMainCategoryDeleteView(BaseAdminDeleteView):
    model = MainCategory
    serializer_class = MainCategorySerializer
    permission_classes = [CanDeleteMainCategory]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin delete item sub categories (requires delete_subcategory permission)
# ===========================================================================================================
class AdminSubCategoryDeleteView(BaseAdminDeleteView):
    model = SubCategory
    serializer_class = SubCategorySerializer
    permission_classes = [CanDeleteSubCategory]
# ===========================================================================================================






# ===========================================================================================================
# BaseAdminCreateView: generic create view + return detail serializer
# ===========================================================================================================
class BaseAdminCreateView(generics.CreateAPIView):
    model = None
    serializer_class = None
    detail_serializer = None
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        detail = self.detail_serializer(instance, context={"request": request})
        return Response({"data": detail.data}, status=status.HTTP_201_CREATED)
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin create new item category type (requires add_categorytype permission)
# ===========================================================================================================
class AdminCategoryTypeCreateView(BaseAdminCreateView):
    model = CategoryType
    serializer_class = CategoryTypeSerializer
    detail_serializer = CategoryTypeWithSubsSerializer
    permission_classes = [CanCreateCategoryType]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin create new item main categories (requires add_maincategory permission)
# ===========================================================================================================
class AdminMainCategoryCreateView(BaseAdminCreateView):
    model = MainCategory
    serializer_class = MainCategorySerializer 
    detail_serializer = MainCategoryWithSubsSerializer
    permission_classes = [CanCreateMainCategory] 
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin create new item sub categories (requires add_subcategory permission)
# ===========================================================================================================
class AdminSubCategoryCreateView(BaseAdminCreateView):
    model = SubCategory
    serializer_class = SubCategorySerializer 
    detail_serializer = SubCategorySerializer
    permission_classes = [CanCreateSubCategory]  
# ===========================================================================================================







# ===========================================================================================================
# BaseAdminUpdateView: generic update view + return updated detail data
# ===========================================================================================================
class BaseAdminUpdateView(generics.UpdateAPIView):
    model = None
    serializer_class = None
    detail_serializer = None
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return self.model.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        updated = self.model.objects.get(id=instance.id)
        detail = self.detail_serializer(updated, context={"request": request})
        return Response(detail.data, status=status.HTTP_200_OK)
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin update item category type (requires change_categorytype permission)
# ===========================================================================================================
class AdminCategoryTypeUpdateView(BaseAdminUpdateView):
    model = CategoryType
    serializer_class = CategoryTypeSerializer
    detail_serializer = CategoryTypeWithSubsSerializer
    permission_classes = [CanUpdateCategoryType]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin update item sub category (requires change_maincategory permission)
# ===========================================================================================================
class AdminMainCategoryUpdateView(BaseAdminUpdateView):
    model = MainCategory
    serializer_class = MainCategorySerializer
    detail_serializer = MainCategoryWithSubsSerializer
    permission_classes = [CanUpdateMainCategory]
# ===========================================================================================================
# 
# ===========================================================================================================
# Admin update item sub categoriy (requires change_subcategory permission)
# ===========================================================================================================
class AdminSubCategoryUpdateView(BaseAdminUpdateView):
    model = SubCategory
    serializer_class = SubCategorySerializer
    detail_serializer = SubCategorySerializer
    permission_classes = [CanUpdateSubCategory]
# ===========================================================================================================








# ===========================================================================================================
# BaseClientList: public list of active items only (status=True)
# ===========================================================================================================
class BaseClientLis(generics.ListAPIView):
    model = None             
    serializer_class = None
    permission_classes = [AllowAny]
    def get_queryset(self):
        return self.model.objects.filter(status=True)   
# ===========================================================================================================
#  
# ===========================================================================================================
# clients get category types items list
# ===========================================================================================================
class ClientCategoryTypeListView(BaseClientLis):
    model = CategoryType
    serializer_class = CategoryTypeSerializer
# ===========================================================================================================
# 
# ===========================================================================================================
# clients get main category tems list
# ===========================================================================================================
class ClientMainCategoryListView(BaseClientLis):
    model = MainCategory
    serializer_class = MainCategorySerializer
# ===========================================================================================================
#   
# ===========================================================================================================
# clients get subcategories items list
# ===========================================================================================================
class ClientSubCategoryListView(BaseClientLis):
    model = SubCategory
    serializer_class = SubCategorySerializer
# ===========================================================================================================





# ===========================================================================================================
# BaseClientDetailView: public item detail for active items
# ===========================================================================================================
class BaseClientDetailView(generics.RetrieveAPIView):
    model = None
    serializer_class = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.model.objects.filter(status=True)
# ===========================================================================================================
# 
# ===========================================================================================================
#  client get main category item
# ===========================================================================================================
class ClientMainCategoryDetailView(BaseClientDetailView):
    model = MainCategory
    serializer_class = MainCategoryWithSubsSerializer
# ===========================================================================================================

# ===========================================================================================================
#  client get category type item
# ===========================================================================================================
class ClientCategoryTypeDetailView(BaseClientDetailView):
    model = CategoryType
    serializer_class = CategoryTypeWithSubsSerializer
# ===========================================================================================================
# 
# 
# ===========================================================================================================
# client get subcategory item
# ===========================================================================================================
class ClientSubCategoryDetailView(BaseClientDetailView):
    model = SubCategory
    serializer_class = SubCategorySerializer
# ===========================================================================================================

# ===========================================================================================================
# get subcategories use filter main foreinkey id & types ManyToMany id
# ===========================================================================================================
class GetsubUseMainAndTypeView(generics.ListAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = CustomDynamicPagination

    def get_queryset(self):
        type_id = self.kwargs.get("type_id")
        main_id = self.kwargs.get("main_id")

        return SubCategory.objects.filter(status=True, main=main_id, types=type_id)
# ===========================================================================================================
