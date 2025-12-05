# =========================================================================================================================================
import django_filters
from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
# from .models import User
from django.contrib.auth import get_user_model
# =========================================================================================================================================

User = get_user_model()


# =========================================================================================================================================
class UserFilter(django_filters.FilterSet):

    # /?first_name=mos | /?first_name=Most | /?first_name=mostafa  etc
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    # /?last_name=bakh | /?last_name=BAKH | /?last_name=bakhouya  etc
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains') 
    # /?username=bakh | /?username=BAKH | /?username=bakhouya  etc
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains') 
    # /?email=mostafa@gmail.com | /?email=Mostafa@gmail.COM   etc
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    # /?phone=0772 | /?phone=0772913984   etc
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    # ===============================================================================================================================
    # /?groups=1&goups=3 
    groups = django_filters.ModelMultipleChoiceFilter(field_name='groups', queryset=Group.objects.all(), conjoined=False  )   
    # /?goup__name=admin | /?goup__name=ADMIN 
    groups__name = django_filters.CharFilter(field_name='groups__name', lookup_expr='icontains')
    # ===============================================================================================================================
    # /?permissions__codename=delete
    permissions__codename = django_filters.CharFilter(field_name='user_permissions__codename', lookup_expr='icontains')   
    # /?permissions__name=Can view
    permissions__name = django_filters.CharFilter(field_name='user_permissions__name', lookup_expr='icontains')
    # ===============================================================================================================================
    # /?is_active=true | /?is_active=false
    is_active = django_filters.BooleanFilter(field_name='is_active')
    # /?is_staff=true | /?is_staff=false
    is_staff = django_filters.BooleanFilter(field_name='is_staff')  
    # /?type_account=admin | /?type_account=personal
    type_account = django_filters.CharFilter(field_name='type_account', lookup_expr='exact')   
    # /?type_account__icontains=admin | /?type_account__icontains=personal  
    # # /?type_account__icontains=ADMIN | /?type_account__icontains=PERSONAL
    type_account__icontains = django_filters.CharFilter(field_name='type_account', lookup_expr='icontains')
    # /?is_superuser=true | /?is_superuser=false
    is_superuser = django_filters.BooleanFilter(field_name='is_superuser')
    # ===============================================================================================================================
    # /?created_at=2025-12-05
    created_at = django_filters.DateFilter(field_name='created_at')   
    # /?created_at__gt=2025-01-01 return  2025-01-02 2025-01-03 2025-01-15 .....
    created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr='gt')
    # /?created_at__gt=2025-01-01 return  2024-12-29, 2024-11-29, 2024-09-15, .....
    created_at__lt = django_filters.DateFilter(field_name='created_at', lookup_expr='lt')
    # /?created_at__gt=2025-01-01 return  2025-01-01 2025-01-03 2025-01-15 .....
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    # /?created_at__gt=2025-01-01 return  2025-01-01, 2024-11-29, 2024-09-15, .....
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    # ===============================================================================================================================
    # /?created_at__year=2025
    created_at__year = django_filters.NumberFilter(field_name='created_at', lookup_expr='year')
    # /?created_at__month=12
    created_at__month = django_filters.NumberFilter(field_name='created_at', lookup_expr='month') 
    # /?created_at__day=5
    created_at__day = django_filters.NumberFilter(field_name='created_at', lookup_expr='day')
    # ===============================================================================================================================

    
    # ========== META CLASS ==========
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'phone',
            
            'groups', 'groups__name', 
            'permissions__codename', 'permissions__name',

            'is_active', 'is_staff', 'is_superuser',
            
            'type_account', 'type_account__icontains',
            
            'created_at', 'created_at__gt', 'created_at__lt', 
            'created_at__gte', 'created_at__lte',
            'created_at__year', 'created_at__month', 'created_at__day',
        ]
        
# =========================================================================================================================================