from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

def home(request):
    context = {
    }
    return render(request, 'home.html', context)

def web_hosting(request):
    return render(request, 'web_hosting.html')

def register_domain(request):
    return render(request, 'register_domain.html')

def transfer_domain(request):
    return render(request, 'transfer_domain.html')

def ssl_certificates(request):
    return render(request, 'ssl_certificates.html')

def whois_lookup(request):
    return render(request, 'whois_lookup.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')
        
        if email and password:
            # Django uses username for authentication, but we want to use email
            # So we need to find the user by email first
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'login.html')
            
            # Authenticate with username and password
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Handle remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms = request.POST.get('terms')
        
        # Validation
        errors = []
        
        if not all([first_name, last_name, email, password, confirm_password]):
            errors.append('Please fill in all required fields.')
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if not terms:
            errors.append('You must accept the Terms of Service and Privacy Policy.')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email address already exists.')
        
        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            errors.extend(e.messages)
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'signup.html')
        
        try:
            # Create user (using email as username for simplicity)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Automatically log in the user
            auth_login(request, user)
            
            messages.success(request, f'Welcome to Hosting Nigeria, {first_name}! Your account has been created successfully.')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def products_services(request):
    return render(request, 'products_services.html')

@login_required
def my_domains(request):
    return render(request, 'my_domains.html')

@login_required
def invoices(request):
    return render(request, 'invoices.html')

@login_required
def support_tickets(request):
    return render(request, 'support_tickets.html')

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

@login_required
def account(request):
    if request.method == 'POST':
        # Handle form submission
        user = request.user
        profile = user.profile
        
        # Update User model fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update UserProfile fields
        profile.phone = request.POST.get('phone', '')
        profile.company = request.POST.get('company', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.country = request.POST.get('country', 'nigeria')
        profile.save()
        
        messages.success(request, 'Your account information has been updated successfully!')
        return redirect('account')
    
    return render(request, 'account.html')

@login_required
def account_security(request):
    return render(request, 'account_security.html')

@login_required
def email_history(request):
    return render(request, 'email_history.html')

@login_required
def user_management(request):
    if request.method == 'POST':
        if 'send_invitation' in request.POST:
            # Handle sending invitation
            invite_first_name = request.POST.get('invite_first_name')
            invite_last_name = request.POST.get('invite_last_name')
            invite_email = request.POST.get('invite_email')
            user_role = request.POST.get('user_role')
            invitation_message = request.POST.get('invitation_message')
            
            # Here you would typically:
            # 1. Create an invitation record in the database
            # 2. Send an email invitation
            # 3. For now, we'll just show a success message
            
            messages.success(request, f'Invitation sent to {invite_email} successfully! They will receive an email with instructions to join your account.')
            return redirect('user_management')
    
    return render(request, 'user_management.html')
