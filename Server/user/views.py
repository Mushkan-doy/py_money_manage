from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializers import *
from .response_handler import ResponseHandler
from .pagination import *
from rest_framework.response import Response
from .aip_utils import get_monthly_expenses, get_yearly_expenses

# Create your views here.
class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    response_handler = ResponseHandler()

    def post(self, request):
        try:
            print("Request Data ::>> ",request.data)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    msg="User Register successfully.",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="Your username or password is wrong.",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in RegisterView: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
    
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    response_handler = ResponseHandler()

    def post(self, request):
        try:
            print("Request Data ::>> ",request.data)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                print("serialize Data ::: ",serializer.data)
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    msg="User Logged in successfully.",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="Your username or password is wrong.",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in LoginView: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
         
class LogoutView(APIView):
    permission_classes = (AllowAny,)
    response_handler = ResponseHandler()

    def post(self, request):
        try:
            print("Request Data ::>> ",request.data)
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            response_dict, status_code = self.response_handler.success(
                data={},
                msg="User Logged out successfully.",
            )
            return Response(
                response_dict,
                status=status_code,
            )
        except Exception as e:
            print(f"Exception in LogoutView: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

class UserProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()

    def put(self, request):
        try:
            print("Request Data ::>>> ",request.data)
            user = request.user
            serializer = self.serializer_class(user, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="Profile has been Updated Successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in UserProfileView: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    
    def put(self, request):
        try:
            print("Request Data :::>>>> ",request.data)
            serializer = self.serializer_class(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="password changed Successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in ChangePasswordView: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
            
# Category CRUD API
class CategoryView(APIView):
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    serializer_class = CategorySerializer
    
    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None
        
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data,context={'request': request})
            if serializer.is_valid():
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="Category has been added successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in CategoryView Add: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
            
    def put(self, request):
        try:
            category_obj = self.get_object(id=request.data['id'])
            if category_obj:
                serializer = self.serializer_class(instance=category_obj, data=request.data, partial=True,context={'request': request})
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
                
            if serializer.is_valid():
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="Category has been updated successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in CategoryView Update: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
            
    def delete(self, request):
        try:
            print("request Data :::>>  ",request.data)
            category_obj = self.get_object(id=request.data['id'])
            if category_obj:
                category_obj.delete()
                response_dict, status_code = self.response_handler.success(
                    data={},
                    error={},
                    msg="Category has been deleted successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in CategoryView Delete: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

class CategoryListView(ListAPIView): 
    queryset = Category.objects.all().order_by('-id')
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    serializer_class = CategorySerializer
    
    # Pagination settings
    pagination_class = CategoryListPagination
    def list(self, request, *args, **kwargs):
        try:
            print("Hello")
            user_obj = User.objects.get(email=self.request.user.email)
            print("user_obj", user_obj)
            queryset = self.queryset.filter(created_by=user_obj)
            page = self.request.query_params.get('page', 1)
            items_per_page = 10  # Adjust this to your desired number of items per page
            page = self.paginate_queryset(queryset)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(queryset, many=True)
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    msg="Page is None.",
                )
            return Response(response_dict, status=status_code)
        
        except Exception as e:
            print(f"Exception in CategoryListView List: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

# Account Settings CRUD API
class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    response_handler = ResponseHandler()
    serializer_class = AccountDetailSerializer

    def get_object(self, id):
        try:
            return AccountDetail.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def post(self, request):
        try:
            print("Request. Data ::: >> ",request.data)
            serializer = self.serializer_class(data=request.data,context={'request':request})
            if serializer.is_valid():
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="AccountDetails has been added successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in AccountDetailView Add: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

    def put(self, request):
        try:
            print("Request. Data ::: >> ",request.data)
            account_detail_obj = self.get_object(id=request.data['id'])
            if account_detail_obj:
                serializer = self.serializer_class(instance=account_detail_obj, data=request.data, context={'request':request}, partial=True)
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )

            if serializer.is_valid():
                serializer.validated_data['created_by'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="AccountDetails has been updated successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in AccountDetailView Update: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

    def delete(self, request):
        try:
            print("request Data :::>>  ",request.data)
            account_detail_obj = self.get_object(id=request.data['id'])
            if account_detail_obj:
                account_detail_obj.delete()
                response_dict, status_code = self.response_handler.success(
                    data={},
                    error={},
                    msg="AccountDetail has been deleted successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in AccountDetailView Delete: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

class AccountDetailListView(ListAPIView):
    queryset = AccountDetail.objects.all().order_by('-id')
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    serializer_class = AccountDetailSerializer

    # Pagination settings
    pagination_class = AccountDetailListPagination

    def list(self, request, *args, **kwargs):
        try:
            print("Hello")
            user_obj = User.objects.get(email=self.request.user.email)
            print("user_obj", user_obj)
            queryset = self.queryset.filter(created_by=user_obj)
            page = self.request.query_params.get('page', 1)
            items_per_page = 10  # Adjust this to your desired number of items per page
            page = self.paginate_queryset(queryset)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(queryset, many=True)
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    msg="Page is None.",
                )
            return Response(response_dict, status=status_code)

        except Exception as e:
            print(f"Exception in AccountDetailListView List: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )


# Get All Category, Transaction Type, and AccountDetails API
class GetAllExpenseDetailsView(APIView):
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()

    def get(self, request):
        try:
            print("Request Data :>> ",request.data)
            # Get All Category User Wise 
            category_arr = []
            category_obj = Category.objects.filter(created_by=request.user)
            print("Category Data :: ",category_obj)
            for co in category_obj:
                category_arr.append({'id': co.id, 'name': co.name})
            print("Category Array :: ",category_arr)
            
            # Get All Account Details 
            account_arr = []
            account_obj = AccountDetail.objects.filter(created_by=request.user)
            print("Account Data :: ",account_obj)
            for ao in account_obj:
                account_arr.append({'id': ao.id, 'name': ao.account_type})
            print("Account Array :: ",account_arr)
            
            # Get All Transaction Type Details
            transaction_arr = []
            transaction_obj = TransactionType.objects.all()
            print("transaction Data :: ",transaction_obj)
            for to in transaction_obj:
                transaction_arr.append({'id': to.id, 'name': to.name})
            print("transaction Array :: ",transaction_arr)
            
            response_dict, status_code = self.response_handler.success(
                data={
                    'category_data': category_arr, 
                    'account_data': account_arr, 
                    'transaction_data': transaction_arr, 
                },
                error={},
                msg="Expense Details has been fetch successfully",
            )
            return Response(
                response_dict,
                status=status_code,
            )

        except Exception as e:
            print(f"Exception in GetAllExpenseDetailsView Get: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

# Expense CRUD API
class ExpenseView(APIView):
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    serializer_class = ExpenseSerializer

    def get_object(self, id):
        try:
            return ExpenseDetails.objects.get(id=id)
        except ExpenseDetails.DoesNotExist:
            return None

    def post(self, request):
        try:
            print("Request Data :>> ",request.data)
            serializer = self.serializer_class(data=request.data,context={'request':request})
            if serializer.is_valid():
                serializer.validated_data['expense_user'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="TransactionDetails has been added successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in ExpenseView Add: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
            
    def put(self, request):
        try:
            print("Request. Data ::: >> ",request.data)
            expense_detail_obj = self.get_object(id=request.data['id'])
            if expense_detail_obj:
                serializer = self.serializer_class(instance=expense_detail_obj, data=request.data, context={'request':request}, partial=True)
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )

            if serializer.is_valid():
                serializer.validated_data['expense_user'] = request.user
                serializer.save()
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    error=serializer.errors,
                    msg="TransactionDetails has been updated successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                response_dict, status_code = self.response_handler.error(
                    data=serializer.data,
                    error=serializer.errors,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in ExpenseView Update: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
    
    def delete(self, request):
        try:
            print("request Data :::>>  ",request.data)
            expense_detail_obj = self.get_object(id=request.data['id'])
            if expense_detail_obj:
                expense_detail_obj.delete()
                response_dict, status_code = self.response_handler.success(
                    data={},
                    error={},
                    msg="TransactionDetails has been deleted successfully",
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
            else:
                err_message = f"This record does not exist(id:{request.data['id']})."
                response_dict, status_code = self.response_handler.error(
                    data=None,
                    error= err_message,
                )
                return Response(
                    response_dict,
                    status=status_code,
                )
        except Exception as e:
            print(f"Exception in ExpenseView Delete: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
       
# Transaction type base API Call 
class ExpenseDetailListView(ListAPIView):
    queryset = ExpenseDetails.objects.all().order_by('-id')
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()
    serializer_class = ExpenseSerializer

    # Pagination settings
    pagination_class = ExpenseDetailListPagination

    def list(self, request, *args, **kwargs):
        try:
            print("Hello")
            transaction_type = request.query_params.get('transaction_type', 2)
            user_obj = User.objects.get(email=self.request.user.email)
            queryset = self.queryset.filter(expense_user=user_obj,expense_type=transaction_type)
            page = self.request.query_params.get('page', 1)
            items_per_page = 10  # Adjust this to your desired number of items per page
            page = self.paginate_queryset(queryset)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                serializer = self.get_serializer(queryset, many=True)
                response_dict, status_code = self.response_handler.success(
                    data=serializer.data,
                    msg="Page is None.",
                )
            return Response(response_dict, status=status_code)

        except Exception as e:
            print(f"Exception in ExpenseDetailListView List: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )
            
# Monthly Report Generate API
import time
class MonthlyReportView(APIView):
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()

    def get(self, request):
        try:
            user_obj = User.objects.get(email=self.request.user.email)
            current_month_year = time.strftime("%Y-%m")
            month = self.request.query_params.get('month', current_month_year) if self.request.query_params.get('month') != "" else current_month_year 
            transaction_type = self.request.query_params.get('transaction_type', 2)
            monthly_expenses = get_monthly_expenses(user_obj, month, transaction_type)
            data = [
                {
                    'month': expense['month'].strftime('%Y-%m'),  # Format the month as 'YYYY-MM'
                    'category': expense['expense_category'],
                    'total_expense': expense['total_expense']
                }
                for expense in monthly_expenses
            ]
            response_dict, status_code = self.response_handler.success(
                data=data,
                error={},
                msg="Monthly Report has been fetch successfully",
            )
            return Response(
                response_dict,
                status=status_code,
            )
        except Exception as e:
            print(f"Exception in MonthlyReportView Add: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )

# Yearly Report Generate API
class YearlyReportView(APIView):
    permission_classes = (IsAuthenticated,)
    response_handler = ResponseHandler()

    def get(self, request):
        try:
            user_obj = User.objects.get(email=self.request.user.email)
            current_year = time.strftime("%Y")
            year = self.request.query_params.get('year', current_year) if self.request.query_params.get('year') != "" else current_year 
            transaction_type = self.request.query_params.get('transaction_type', 2)
            monthly_expenses = get_yearly_expenses(user_obj, year, transaction_type)
            data = [
                {
                    'year': expense['year'].strftime('%Y'),  # Format the month as 'YYYY-MM'
                    'category': expense['expense_category'],
                    'total_expense': expense['total_expense']
                }
                for expense in monthly_expenses
            ]
            response_dict, status_code = self.response_handler.success(
                data=data,
                error={},
                msg="Monthly Report has been fetch successfully",
            )
            return Response(
                response_dict,
                status=status_code,
            )
        except Exception as e:
            print(f"Exception in MonthlyReportView Add: \n {e}")
            response_dict, status_code = self.response_handler.failure(
                data=None, error=None, msg="Something went wrong."
            )
            return Response(
                response_dict,
                status=status_code,
            )