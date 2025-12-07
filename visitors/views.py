
# ===========================================================================================
# ===========================================================================================
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status, generics

from visitors.permissions import CanDeleteVisitor, CanViewListVisitor, CanViewVisitor
from .models import Visitor
from .serializers import VisitorSerializer, VisitorDetailSerializer
# ===========================================================================================


# ===========================================================================================
# TrackVisitAPIView
# This class represents an API for tracking visitor visits.
# It uses the GET method to record a visitor's visit when they enter any page.
# Steps:
    # 1. Call the record_visit function from the Visitor form manager to record or update the visitor.
    # 2. Get the recorded or updated visitor object.
    # 3. Use VisitorSerializer to convert the visitor data into a sendable JSON format.
    # 4. Return a response with information about the visitor:
        # - success: Request successful status
        # - visitor: Structured visitor data
        # - is_new_visitor: Is the visitor new or existing?
        # - is_new_visit: Is this a new visit within the last 24 hours?
    # 5. Response status: HTTP 200 upon success.
# ===========================================================================================
class TrackVisitAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = Visitor.objects.record_visit(request, page_visited=request.path)
        visitor = result['visitor']
        serialized_visitor = VisitorSerializer(visitor).data

        return Response({
            'success': True,
            'visitor': serialized_visitor,
            'is_new_visitor': result['is_new_visitor'],
            'is_new_visit': result['is_new_visit'],
        }, status=status.HTTP_200_OK)
# ===========================================================================================
# 
# 
# 
# ===========================================================================================
# Fetch all visitors (comprehensive view)
# - Only registered users with administrative privileges are allowed.
# - The CanViewListVisitor permission determines whether a user is authorized to view the list.
# ===========================================================================================
class VisitorListVisitors(generics.ListAPIView):
    serializer_class = VisitorDetailSerializer
    queryset = Visitor.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewListVisitor]
# ===========================================================================================
# 
# 
# 
# ===========================================================================================
# Fetch data for a specific visitor
# - Displays information for a single visitor based on the identifier (id).
# - Protected by administrative privileges and the CanViewVisitor custom view permission.
# ===========================================================================================
class VisitorDetailVisitor(generics.RetrieveAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, CanViewVisitor]
# ===========================================================================================
# 
# 
# 
# ===========================================================================================
# Delete a visitor from the system
# - Only administrators with deletion privileges are permitted.
# - Deletes the visitor's history and all associated visits.
# ===========================================================================================
class VisitorDeleteVisitor(generics.DestroyAPIView):
    serializer_class = VisitorDetailSerializer
    queryset = Visitor.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser, CanDeleteVisitor]
# ===========================================================================================
