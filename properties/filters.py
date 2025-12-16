from django_filters import rest_framework as filters
from .models import Property
from django.db.models import Q


# ==============================================================================
# Filter properties 
# ==============================================================================
class PropertyFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    city = filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    category_type = filters.CharFilter(field_name='category_type__name', lookup_expr='icontains')
    main_category = filters.CharFilter(field_name='main_category__name', lookup_expr='icontains')
    sub_category = filters.CharFilter(field_name='sub_category__name', lookup_expr='icontains')
    price_type = filters.CharFilter(field_name='price_type__name', lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')   
    min_area = filters.NumberFilter(field_name='area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='area', lookup_expr='lte')
    created_at = filters.DateFilter(field_name='created_at')
    created_at__gt = filters.DateFilter(field_name='created_at', lookup_expr='gt')
    created_at__lt = filters.DateFilter(field_name='created_at', lookup_expr='lt')
    created_at__gte = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    created_at__year = filters.NumberFilter(field_name='created_at', lookup_expr='year')
    created_at__month = filters.NumberFilter(field_name='created_at', lookup_expr='month')
    created_at__day = filters.NumberFilter(field_name='created_at', lookup_expr='day')
    price_range = filters.CharFilter(method='filter_price_range', label="نطاق السعر")

    class Meta:
        model = Property
        fields = [
            'title', 'description', 'address',
            'city', 'category_type', 'main_category', 'sub_category', 'price_type', 
            'min_price', 'max_price', 'min_area', 'max_area',
            'created_at', 'created_at__gt', 'created_at__lt', 'created_at__gte', 'created_at__lte',
            'created_at__year', 'created_at__month', 'created_at__day',           
        ]
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(address__icontains=value) |
            Q(city__name__icontains=value) |
            Q(category_type__name__icontains=value) |
            Q(main_category__name__icontains=value) |
            Q(sub_category__name__icontains=value) |
            Q(price_type__name__icontains=value) |
            Q(user__username__icontains=value)
        ).distinct()
    
    def filter_price_range(self, queryset, name, value):
        try:
            if '-' in value:
                min_price, max_price = value.split('-')
                return queryset.filter(price__gte=min_price, price__lte=max_price)
        except (ValueError, AttributeError):
            pass
        return queryset

# ==============================================================================




