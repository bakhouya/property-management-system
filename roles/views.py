from django.contrib.auth.models import Group, Permission
from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from roles.permissions import CanCreateGroup, CanDeleteGroup, CanUpdateGroup, CanViewGroup
from .serializers import PermissionSerializer, GroupSerializer

# ============================================================================================
# Get all permissions for just read 
# The CanCreateGroup and CanUpdateGroup permissions were used here because they are only needed for the processes of creating and updating groups.
# A custom response was created to display permissions in an organized manner for each model,
# by grouping the permissions of each model and returning them in an organized and clear way instead of the
# default format which is less clear to the user or the front end.
# ============================================================================================
class PermissionListView(views.APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, CanCreateGroup, CanUpdateGroup] 
    

    def get(self, request):
        content_types = ContentType.objects.filter(permission__isnull=False).distinct().order_by('app_label', 'model')
        
        result = []
        for contentType in content_types:
            permissions = Permission.objects.filter(content_type=contentType)
            
            if permissions.exists():
                model_class = contentType.model_class()
                model_verbose = model_class._meta.verbose_name if model_class else contentType.model
                
                result.append({
                    'app_label': contentType.app_label,
                    'model_name': contentType.model,
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
# In this section, we've presented all groups in an organized manner,
# with pre-loaded permissions and users associated with each group to improve performance.
# We've also added simple statistics (number of groups, number of users, and number of permissions)
# to provide clearer information for the control panel.
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
# This section is designed to retrieve data for a single group by ID, returning additional details 
# such as the number of users and their associated permissions.
# The prefetch_related feature was used to improve performance, and errors were addressed to ensure a
#  clear response if the group is not found or another error occurs.
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
# This process creates a new group with its own permissions.
# Data is checked before saving, and the created group is then returned.
# Error handling has been added to ensure an appropriate response should any problem occur during the process.
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
# This section is for updating the data of a specific group via ID.
# The group is loaded first, and then the new data is verified before being saved.
# Error handling has been added to ensure a clear response if any errors occur during the update process.
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
# This section is responsible for deleting a specific group based on its ID.
# The process is protected by the necessary permissions to ensure that only an authorized user can perform the deletion.
# ============================================================================================
class GroupDeleteView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteGroup]
    lookup_field = 'id'
# ============================================================================================

