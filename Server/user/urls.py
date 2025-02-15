from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # Users related urls.
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # Login User
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('update-profile', UserProfileView.as_view(), name='update_profile'),
    path('change-password', ChangePasswordView.as_view(), name='change_password'),
    
    
    # Category Crud
    path('category', CategoryView.as_view(), name='category'),
    path('list-category', CategoryListView.as_view(), name='list_category'),

    # AccountDetail Crud
    path('account-details', AccountDetailsView.as_view(), name='account_details'),
    path('list-account-details', AccountDetailListView.as_view(), name='list_account_details'),

    # Expense Details Crud
    path('get-all-details', GetAllExpenseDetailsView.as_view(), name='get_all_details'),
    path('add-transaction', ExpenseView.as_view(), name='add_transaction'),
    path('list-transaction-details', ExpenseDetailListView.as_view(), name='list_transaction_details'),
    
    # Monthly and Yearly base Report
    path('monthly-report', MonthlyReportView.as_view(), name='monthly_report'),
    path('yearly-report', YearlyReportView.as_view(), name='yearly_report'),

]
