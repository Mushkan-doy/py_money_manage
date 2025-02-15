import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'role_type'
        verbose_name_plural = 'role type'

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Public identifier')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=500)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
    
# Category Table
class Category(models.Model):
    name = models.CharField(max_length=500, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="created_by")
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'category'

    def __str__(self):
        return self.name

# Transaction Type Table
class TransactionType(models.Model):
    name = models.CharField(max_length=500, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transaction Type'

    def __str__(self):
        return self.name

# AccountDetails Table
class AccountDetail(models.Model):
    account_type = models.CharField(max_length=100, blank=False)
    account_amount = models.FloatField(null=True, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="account_created_by")
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'AccountDetails'
        verbose_name_plural = 'AccountDetails'

    def __str__(self):
        return self.account_type
    
class ExpenseDetails(models.Model):
    expense_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    expense_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    expense_amount = models.FloatField(null=True, blank=False)
    expense_account = models.ForeignKey(AccountDetail, on_delete=models.CASCADE, blank=True, null=True)
    expense_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, blank=True, null=True)
    expense_from = models.ForeignKey(AccountDetail, on_delete=models.CASCADE, blank=True, null=True, related_name="expense_from")
    expense_to = models.ForeignKey(AccountDetail, on_delete=models.CASCADE, blank=True, null=True, related_name="expense_to")
    expense_date = models.DateTimeField(blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        verbose_name = 'ExpenseDetails'
        verbose_name_plural = 'ExpenseDetails'