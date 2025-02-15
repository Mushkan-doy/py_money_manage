from django.contrib import admin
from .models import *
from .forms import *

from django.contrib.auth import authenticate
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm  
    model = User

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'email_verified', 'is_delete')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role', 'email_verified',)}),
        # ('Personal Info', {'fields': ('created_by',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active',
                        'is_delete', 'email_verified')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    

admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)

# category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created_by', 'created_on','update_on'
    )

    class Meta:
        model = Category

# Transaction Type
@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'created_on','update_on'
    )

    class Meta:
        model = TransactionType

# Account Details
@admin.register(AccountDetail)
class AccountDetailAdmin(admin.ModelAdmin):
    list_display = (
        'account_type', 'account_amount','created_by', 'created_on','update_on'
    )

    class Meta:
        model = AccountDetail       

# Expense Details
@admin.register(ExpenseDetails)
class ExpenseDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'expense_user', 'expense_category', 'expense_amount', 'expense_account', 'expense_type', 'expense_from', 'expense_to', 'expense_date', 'note', 'created_on', 'update_on'
    )

    class Meta:
        model = ExpenseDetails