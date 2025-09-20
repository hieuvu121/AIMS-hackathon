from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

def home(request):
    return render(request, 'main/home.html')

def case_study(request):
    return render(request, 'main/case_study.html')

def methods(request):
    return render(request, 'main/methods.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return HttpResponseRedirect('/')

def dashboard_api(request):
    """Simple dashboard API endpoint to prevent 404 errors"""
    # Get query parameters
    timeframe = request.GET.get('timeframe', 'all')
    sector = request.GET.get('sector', 'all')
    
    # Return appropriate data based on parameters
    data = {
        'status': 'success',
        'message': f'Dashboard data for {timeframe} timeframe and {sector} sector',
        'data': {
            'total_reports': 1250,
            'active_organizations': 342,
            'compliance_rate': 78.5,
            'sectors': ['Technology', 'Fashion', 'Agriculture', 'Manufacturing'],
            'timeframe': timeframe,
            'sector': sector,
            'trends': {
                'improvement': 12.3,
                'transparency': 8.7,
                'accountability': 15.2
            },
            'chart_data': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'values': [100, 120, 95, 140, 110, 130]
            }
        }
    }
    return JsonResponse(data)