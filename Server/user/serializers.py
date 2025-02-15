from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
import re

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "role",
        )

    
    
    def validate_email(self, value):
        if value:
            return value.lower()
        return value

    def validate(self, attrs):
        print("attrs: - ", attrs)
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        # validating password
        password_val = attrs["password"]
        regex_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%*?#&]{6,14}$"
        is_email_regex_match = re.match(regex_pattern, password_val)
        if not is_email_regex_match:
            raise serializers.ValidationError(
                {
                    "password": "Password Length must be 6-14 characters"
                    # "password": "Password Length must be 6-14 characters, at least 1 caps, 1 small, 1 special char, 1 number."
                }
            )
        return attrs 

    def validate_role(self, value):
        try:
            print("Role value", value, type(value))
            role_list = [1,2]
            if value.id in role_list:
                role_obj = Role.objects.get(id=value.id)
                return value
        except Role.DoesNotExist:
            raise serializers.ValidationError("Invalid role.")
    
    def create(self, validated_data):
        print("validated_data: - ", validated_data)
        validated_data.pop("confirm_password")
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        print(f"create userObj 2:- {user}")
        print(f"create userObj type 2:- {type(user)}")
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_date):
        pass
    def update(self, instance, validated_data):
        pass
    
    def validate_email(self, value):
        try:
            User.objects.get(email__iexact=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("This account doesn't exist. Please create a new account.")
            )
        return value

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try: 
            user_obj = User.objects.get(email=user.email)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            update_last_login(None, user)
            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'id': user.id,
            }
            return validation
        except:
            raise serializers.ValidationError("Invalid ")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "role",
        )
        
    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, allow_null=False)
    password = serializers.CharField(
        required=True,
        allow_null=False,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?#&])[A-Za-z\d@$!%*?#&]{6,14}$",
                message="Password must contain 6-14 character, atleast 1 Caps, 1 Small, 1 Special Character, 1 Number.",
            )
        ],
    )
    confirm_password = serializers.CharField(required=True, allow_null=False)

    def validate_old_password(self, value):
        """
        Validate that the old_password field is correct.
        """
        old_password = value
        if not self.context.get("request").user.check_password(old_password):
            raise serializers.ValidationError(_("Your old password is incorrect."))
        return old_password

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Password fields didn't match."}
            )
        return attrs
    
    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "created_by"
        )
        
    def get_created_by(self, obj):
        user_obj = User.objects.get(id=obj.created_by.id)
        user_email = user_obj.email
        return user_email


class AccountDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    class Meta:
        model = AccountDetail
        fields = (
            "account_type",
            "account_amount",
            "created_by",
        )
    def get_created_by(self, obj):
        user_obj = User.objects.get(id=obj.created_by.id)
        user_email = user_obj.email
        return user_email

class ExpenseSerializer(serializers.ModelSerializer):
    expense_user = serializers.SerializerMethodField()
    class Meta:
        model = ExpenseDetails
        fields = (
            "expense_user",
            "expense_category",
            "expense_amount",
            "expense_account",
            "expense_type",
            "expense_from",
            "expense_to",
            "expense_date",
            "note",
        )
    def get_expense_user(self, obj):
        user_obj = User.objects.get(id=obj.expense_user.id)
        user_email = user_obj.email
        return user_email

    def get_expense_date(self, obj):
        value = obj.expense_date
        formatted_date_string = value.strftime("%d-%b-%Y %I:%M:%S %p")
        return formatted_date_string
    