from django.contrib.auth.models import Group, Permission
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from roles.permissions import CanCreateGroup, CanDeleteGroup, CanUpdateGroup, CanViewGroup
from .serializers import PermissionSerializer, GroupSerializer

# ============================================================================================
# Get all permissions for just red 
# ============================================================================================
class PermissionListView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    
    def get(self, request):
        content_types = ContentType.objects.filter(permission__isnull=False).distinct().order_by('app_label', 'model')
        
        result = []
        for ct in content_types:
            permissions = Permission.objects.filter(content_type=ct)
            
            if permissions.exists():
                model_class = ct.model_class()
                model_verbose = model_class._meta.verbose_name if model_class else ct.model
                
                result.append({
                    'app_label': ct.app_label,
                    'model_name': ct.model,
                    'model_verbose': model_verbose,
                    'permissions': PermissionSerializer(permissions, many=True).data
                })
        
        total_permissions = Permission.objects.count()
        total_models = len(result)
        
        return Response({
            'data': result,
            'stats': {
                'total_permissions': total_permissions,
                'total_models': total_models,
                'permissions_per_model': round(total_permissions / total_models, 2) if total_models > 0 else 0
            }
        }, status=status.HTTP_200_OK)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# get all groups
# ============================================================================================
class GroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions', 'user_set')
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            total_groups = queryset.count()
            total_users = sum(group.user_set.count() for group in queryset)
            total_permissions = sum(group.permissions.count() for group in queryset)
            
            return Response({
                'data': serializer.data,
                'stats': {
                    'total_groups': total_groups,
                    'total_users': total_users,
                    'total_permissions': total_permissions,   
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e),}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
#  get itme group by id
# ============================================================================================
class GroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewGroup]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions', 'user_set')
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response({
                'data': serializer.data,
                'details': {
                    'users_count': instance.user_set.count(),
                    'permissions_count': instance.permissions.count(),
                }
            }, status=status.HTTP_200_OK)
        
        except Group.DoesNotExist:
            return Response({"error": "Data not fount"}, status=status.HTTP_404_NOT_FOUND)  
            
        except Exception as e:
            return Response({'error': str(e),}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# create new group with permissions
# ============================================================================================
class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanCreateGroup]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            group = serializer.save()
            
            return Response({'data': GroupSerializer(group).data}, status=status.HTTP_201_CREATED)  
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
# Update group item by id
# ============================================================================================
class GroupUpdateView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanUpdateGroup]
    lookup_field = 'id'
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            group = serializer.save()
            
            return Response({'data': GroupSerializer(group).data})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# ============================================================================================
# 
# 
# 
# 
# ============================================================================================
#  delete group item by id
# ============================================================================================
class GroupDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteGroup]
    lookup_field = 'id'
# ============================================================================================

