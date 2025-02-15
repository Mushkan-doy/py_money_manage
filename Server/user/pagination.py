from rest_framework import pagination
from rest_framework.response import Response
from user.response_handler import ResponseHandler


class CategoryListPagination(pagination.PageNumberPagination):
    response_handler = ResponseHandler()
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 5000

    def get_paginated_response(self, data):
        context = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }
        response_dict, status_code = self.response_handler.success(
            data=context,
            msg="Category data fetched successfully!",
        )
        return Response(response_dict)

class AccountDetailListPagination(pagination.PageNumberPagination):
    response_handler = ResponseHandler()
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 5000

    def get_paginated_response(self, data):
        context = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }
        response_dict, status_code = self.response_handler.success(
            data=context,
            msg="AccountDetail data fetched successfully!",
        )
        return Response(response_dict)
    

class ExpenseDetailListPagination(pagination.PageNumberPagination):
    response_handler = ResponseHandler()
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 5000

    def get_paginated_response(self, data):
        context = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }
        response_dict, status_code = self.response_handler.success(
            data=context,
            msg="TransactionDetail data fetched successfully!",
        )
        return Response(response_dict)