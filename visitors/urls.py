from django.urls import path
from .views import TrackVisitAPIView, VisitorListVisitors, VisitorDeleteVisitor, VisitorDetailVisitor

urlpatterns = [
    # track and get data visitor and visit
    path('visitors/track/', TrackVisitAPIView.as_view(), name='visitor-track'),
    # get all lis visitors with visitis: admin  
    path('ad/visitors/', VisitorListVisitors.as_view(), name='visitor_list'),
    # get visitor item data with visits: admin
    path('ad/visitors/<uuid:pk>/', VisitorDetailVisitor.as_view(), name='view_visitor'),
    # delete visitor item with visits : admin 
    path('ad/visitors/<uuid:pk>/delete/', VisitorDeleteVisitor.as_view(), name='delete_visitor'),
]

