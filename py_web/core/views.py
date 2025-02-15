from django.shortcuts import render
from .forms import LoginForm
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    api_domain = settings.API_DOMAIN
    return render(request, 'accounts/login.html',{'form': form, 'msg': msg, 'api_domain': api_domain})

def register_view(request):
    # form = LoginForm(request.POST or None)
    # msg = None
    # api_domain = settings.API_DOMAIN
    return render(request, 'accounts/register.html')

def dashboard_view(request):
    # form = LoginForm(request.POST or None)
    # msg = None
    # api_domain = settings.API_DOMAIN
    return render(request, 'pages/dashboard.html')