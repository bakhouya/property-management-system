from django.urls import path
from .views import (
    AdminCategoryTypeListView, AdminCategoryTypeCreateView, AdminCategoryTypeUpdateView, AdminCategoryTypeDeleteView, AdminCategoryTypeDetailView,
    ClientCategoryTypeListView, ClientCategoryTypeDetailView,
    AdminMainCategoryListView, AdminMainCategoryCreateView, AdminMainCategoryUpdateView, AdminMainCategoryDeleteView, AdminMainCategoryDetailView,
    ClientMainCategoryListView, ClientMainCategoryDetailView,
    AdminSubCategoryListView, AdminSubCategoryCreateView, AdminSubCategoryUpdateView, AdminSubCategoryDeleteView, AdminSubCategoryDetailView,
    ClientSubCategoryListView, ClientSubCategoryDetailView, GetsubUseMainAndTypeView
)







urlpatterns = [
    # =========================================================================================================
    # urls for control categories type from admin panel with handle permissions
    path("ad/categories/types/", AdminCategoryTypeListView.as_view(), name="categories types admin"),
    path("ad/categories/types/create/", AdminCategoryTypeCreateView.as_view(), name="category-type-create"),
    path("ad/categories/types/<uuid:pk>/", AdminCategoryTypeDetailView.as_view(), name="category-type-details"),
    path("ad/categories/types/<uuid:pk>/update/", AdminCategoryTypeUpdateView.as_view(), name="category-type-update"),
    path("ad/categories/types/<uuid:pk>/delete/", AdminCategoryTypeDeleteView.as_view(), name="category-type-delete"),
    # url to get categoryes for clients    
    path("categories/types/", ClientCategoryTypeListView.as_view(), name="categories-types-general"),
    path("categories/types/<uuid:pk>/", ClientCategoryTypeDetailView.as_view(), name="category-type-details-general"),
    # =========================================================================================================


    # =========================================================================================================
    # urls for control main categories from admin panel with handle permissions
    path("ad/categories/main/", AdminMainCategoryListView.as_view(), name="categories types admin"),
    path("ad/categories/main/create/", AdminMainCategoryCreateView.as_view(), name="category-type-create"),
    path("ad/categories/main/<uuid:pk>/", AdminMainCategoryDetailView.as_view(), name="category-type-details"),
    path("ad/categories/main/<uuid:pk>/update/", AdminMainCategoryUpdateView.as_view(), name="category-type-update"),
    path("ad/categories/main/<uuid:pk>/delete/", AdminMainCategoryDeleteView.as_view(), name="category-type-delete"),
    # url to get categoryes for clients    
    path("categories/main/", ClientMainCategoryListView.as_view(), name="categories-types-general"),
    path("categories/main/<uuid:pk>/", ClientMainCategoryDetailView.as_view(), name="category-type-details-general"),
    # =========================================================================================================


    # =========================================================================================================
    # urls for control sub categories from admin panel with handle permissions
    path("ad/categories/sub/", AdminSubCategoryListView.as_view(), name="categories-sub-admin"),
    path("ad/categories/sub/create/", AdminSubCategoryCreateView.as_view(), name="category-sub-create"),
    path("ad/categories/sub/<uuid:pk>/", AdminSubCategoryDetailView.as_view(), name="category-sub-details"),
    path("ad/categories/sub/<uuid:pk>/update/", AdminSubCategoryUpdateView.as_view(), name="category-sub-update"),
    path("ad/categories/sub/<uuid:pk>/delete/", AdminSubCategoryDeleteView.as_view(), name="category-sub-delete"),
    # url to get categoryes for clients    
    path("categories/sub/", ClientSubCategoryListView.as_view(), name="categories-sub-general"),
    path("categories/sub/<uuid:pk>/", ClientSubCategoryDetailView.as_view(), name="category-sub-details-general"),
    # =========================================================================================================


    path("types/<uuid:type_id>/main/<uuid:main_id>/sub/all/", GetsubUseMainAndTypeView.as_view(), name="filtered-subcategories",)


]
