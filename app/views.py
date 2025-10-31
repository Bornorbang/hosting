from django.shortcuts import render

def home(request):
    context = {
    }
    return render(request, 'home.html', context)

def web_hosting(request):
    return render(request, 'web_hosting.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

# Support Pages
def contact_us(request):
    return render(request, 'contact_us.html')

def help_center(request):
    return render(request, 'help_center.html')

def knowledge_base(request):
    return render(request, 'knowledge_base.html')

# Company Pages
def about_us(request):
    return render(request, 'about_us.html')

def blog(request):
    return render(request, 'blog.html')

def careers(request):
    return render(request, 'careers.html')

# Legal Pages
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

def refund_policy(request):
    return render(request, 'refund_policy.html')
