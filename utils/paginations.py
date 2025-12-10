
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



# ==================================================================================
# Custom pagination users 
# ==================================================================================
class CustomDynamicPagination(PageNumberPagination):
    # number items in each page
    page_size = 10  
    # option url change page size pagination /api/accounts/ad/users/?page_size=10 
    page_size_query_param = 'page_size' 
    # max page size can user custom  => /api/accounts/ad/users/?page_size=100 => stop
    max_page_size = 100  
    
    def get_paginated_response(self, data):
        return Response({
            'pagination': {
                'next': self.get_next_link(),                   # url next page
                'previous': self.get_previous_link(),           # url previous page
                'count': self.page.paginator.count,             # count all items in databse 
                'total_pages': self.page.paginator.num_pages,   # count pages paginations
                'current_page': self.page.number,               # number this page 
                'page_size': self.page.paginator.per_page,      # count items in this page 
            },
            'results': data
        })
# ==================================================================================
