from django_filters import rest_framework as filters
from .models import Property
from decimal import Decimal
import django_filters

class PropertyFilter(filters.FilterSet):
    # فلاتر البحث الأساسية
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    
    # فلاتر العلاقات
    user = filters.NumberFilter(field_name='user__id')
    user_username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    
    # فلاتر الفئات
    category_type = filters.NumberFilter(field_name='category_type__id')
    main_category = filters.NumberFilter(field_name='main_category__id')
    sub_category = filters.NumberFilter(field_name='sub_category__id')
    city = filters.NumberFilter(field_name='city__id')
    city_name = filters.CharFilter(field_name='city__name', lookup_expr='icontains')
    
    # فلاتر السعر
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_type = filters.NumberFilter(field_name='price_type__id')
    
    # فلاتر المساحة
    min_area = filters.NumberFilter(field_name='area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='area', lookup_expr='lte')
    
    # فلاتر البوابية
    status = filters.BooleanFilter(field_name='status')
    is_blocked = filters.BooleanFilter(field_name='is_blocked')
    is_owner = filters.BooleanFilter(field_name='is_owner')
    
    # فلاتر التواريخ
    created_after = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_after = filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = filters.DateFilter(field_name='updated_at', lookup_expr='lte')
    
    # فلتر حسب الشعبية (عدد الإعجابات)
    min_likes = filters.NumberFilter(method='filter_min_likes')
    max_likes = filters.NumberFilter(method='filter_max_likes')
    
    # فلتر حسب المشاهدات
    min_views = filters.NumberFilter(method='filter_min_views')
    max_views = filters.NumberFilter(method='filter_max_views')
    
    # فلتر حسب العنوان الكامل
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    
    # فلتر للترتيب
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('price', 'price'),
            ('area', 'area'),
            ('title', 'title'),
        ),
        field_labels={
            'created_at': 'تاريخ الإنشاء',
            'updated_at': 'تاريخ التحديث',
            'price': 'السعر',
            'area': 'المساحة',
            'title': 'العنوان',
        }
    )
    
    class Meta:
        model = Property
        fields = {
            'title': ['exact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'area': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'status': ['exact'],
            'is_blocked': ['exact'],
            'is_owner': ['exact'],
        }
    
    def filter_min_likes(self, queryset, name, value):
        """فلتر حسب الحد الأدنى لعدد الإعجابات"""
        return queryset.annotate(
            likes_count=django_filters.Count('likes')
        ).filter(likes_count__gte=value)
    
    def filter_max_likes(self, queryset, name, value):
        """فلتر حسب الحد الأقصى لعدد الإعجابات"""
        return queryset.annotate(
            likes_count=django_filters.Count('likes')
        ).filter(likes_count__lte=value)
    
    def filter_min_views(self, queryset, name, value):
        """فلتر حسب الحد الأدنى لعدد المشاهدات"""
        return queryset.annotate(
            views_count=django_filters.Count('views')
        ).filter(views_count__gte=value)
    
    def filter_max_views(self, queryset, name, value):
        """فلتر حسب الحد الأقصى لعدد المشاهدات"""
        return queryset.annotate(
            views_count=django_filters.Count('views')
        ).filter(views_count__lte=value)
    
    # فلتر متقدم للسعر حسب النطاق
    price_range = filters.CharFilter(method='filter_price_range')
    
    def filter_price_range(self, queryset, name, value):
        """فلتر متقدم للسعر حسب النطاق (مثال: "1000-5000")"""
        try:
            if '-' in value:
                min_price, max_price = value.split('-')
                min_price = Decimal(min_price.strip())
                max_price = Decimal(max_price.strip())
                return queryset.filter(price__gte=min_price, price__lte=max_price)
        except (ValueError, AttributeError):
            pass
        return queryset
    
    # فلتر متقدم للبحث في عدة حقول
    search = filters.CharFilter(method='filter_search')
    
    def filter_search(self, queryset, name, value):
        """فلتر بحث متقدم في عدة حقول"""
        return queryset.filter(
            filters.Q(title__icontains=value) |
            filters.Q(description__icontains=value) |
            filters.Q(address__icontains=value) |
            filters.Q(city__name__icontains=value) |
            filters.Q(user__username__icontains=value)
        ).distinct()