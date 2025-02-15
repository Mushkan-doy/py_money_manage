from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils.dateparse import parse_date
from .models import ExpenseDetails
from datetime import timedelta, datetime

def get_monthly_expenses(user_obj, month_str=None, transaction_type=None):
    # If no month is passed, use the current month
    if month_str is None:
        # Get the current month in 'YYYY-MM' format
        month_str = datetime.now().strftime('%Y-%m')

    # Parse the passed month into a datetime object
    try:
        # The month_str format should be 'YYYY-MM'
        month_start_date = parse_date(f"{month_str}-01")  # Create a date object for the 1st of the given month
        month_end_date = month_start_date.replace(day=28) + timedelta(days=4)  # Last day of the month
        month_end_date = month_end_date - timedelta(days=month_end_date.day)  # Get the last day of the month
    except ValueError:
        raise ValueError("Invalid month format. Please use 'YYYY-MM' format.")

    
    filters = {
        'expense_user': user_obj,
        'created_on__gte': month_start_date,
        'created_on__lte': month_end_date
    }

    if transaction_type:
        filters['expense_type'] = transaction_type 

    # Step 1: Get the total expenses per month and category
    monthly_expenses_category = (
        ExpenseDetails.objects
        .filter(**filters)
        # .filter(expense_user=user_obj, created_on__gte=month_start_date, created_on__lte=month_end_date)
        .annotate(month=TruncMonth('created_on'))
        .values('month', 'expense_category')
        .annotate(total_expense=Sum('expense_amount'))
        .order_by('month', 'expense_category')
    )

    # Step 2: Restructure the result into the desired format
    result = []
    current_month = None
    month_data = {}
    monthly_total = 0

    # Loop through the queryset and organize the data
    for entry in monthly_expenses_category:
        month = entry['month']
        category = entry['expense_category']
        total_expense = entry['total_expense']
        
        # If we're in a new month, store the previous month's data and reset the current month
        if month != current_month:
            if current_month is not None:
                result.append({'month': current_month,'total_monthly_amount': monthly_total, 'expense_category': list(month_data.values())})
            
            current_month = month
            month_data = {}
            monthly_total = 0

        # Add the category data for the current month
        month_data[category] = {'name': category, 'total_expense': total_expense}
        monthly_total += total_expense
        
    # Add the last month's data
    if current_month is not None:
        result.append({'month': current_month, 'expense_category': list(month_data.values()), 'total_expense': monthly_total})

    return result


def get_yearly_expenses(user_obj, year_str=None, transaction_type=None):
    if year_str is None:
        year_str = datetime.now().strftime('%Y')

    try:
        year_start_date = parse_date(f"{year_str}-01-01")
        year_end_date = year_start_date.replace(month=12, day=31)
    except ValueError:
        raise ValueError("Invalid year format. Please use 'YYYY' format.")

    # Step 1: Get the total expenses per year and category, optionally filtered by transaction type
    filters = {
        'expense_user': user_obj,
        'created_on__gte': year_start_date,
        'created_on__lte': year_end_date
    }

    if transaction_type:
        filters['expense_type'] = transaction_type  # Apply transaction type filter if provided
    
    yearly_expenses_category = (
        ExpenseDetails.objects
        .filter(**filters)  # Apply the dynamic filters
        .annotate(year=TruncYear('created_on'))
        .values('year', 'expense_category')
        .annotate(total_expense=Sum('expense_amount'))
        .order_by('year', 'expense_category')
    )

    # Step 2: Restructure the result into the desired format
    result = []
    current_year = None
    year_data = {}
    yearly_total = 0

    # Loop through the queryset and organize the data
    for entry in yearly_expenses_category:
        year = entry['year']
        category = entry['expense_category']
        total_expense = entry['total_expense']
        
        # If we're in a new year, store the previous year's data and reset the current year
        if year != current_year:
            if current_year is not None:
                result.append({'year': current_year, 'total_yearly_amount': yearly_total, 'expense_category': list(year_data.values())})
            
            current_year = year
            year_data = {}
            yearly_total = 0

        # Add the category data for the current year
        year_data[category] = {'name': category, 'total_expense': total_expense}
        yearly_total += total_expense
        
    # Add the last year's data
    if current_year is not None:
        result.append({'year': current_year, 'expense_category': list(year_data.values()), 'total_expense': yearly_total})

    return result


