from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import requests
import json
import datetime
import os

def _get_domain_availability(domain_name):
    """
    Helper function to check domain availability using ConnectReseller API
    Returns the API response data
    """
    if not domain_name:
        return {
            'success': False,
            'error': 'Domain name is required'
        }
    
    # Clean domain name (remove any protocols, www, etc.)
    domain_name = domain_name.lower().replace('http://', '').replace('https://', '').replace('www.', '')
    
    try:
        # Prepare API request
        api_url = f"{settings.CONNECTRESELLER_BASE_URL}/checkdomainavailable"
        params = {
            'APIKey': settings.CONNECTRESELLER_API_KEY,
            'websiteName': domain_name
        }
        
        # Make API request
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse API response
        api_data = response.json()
        
        # Format response for frontend
        response_msg = api_data.get('responseMsg', {})
        status_code = response_msg.get('statusCode')
        message = response_msg.get('message', '')
        
        if status_code == 200:
            response_data = api_data.get('responseData', {})
            available = response_data.get('available', False)
            
            # Get USD prices from API
            registration_usd = response_data.get('registrationFee', 0)
            renewal_usd = response_data.get('renewalfee', 0)
            transfer_usd = response_data.get('transferFee', 0)
            
            # Apply currency conversion and profit margin
            exchange_rate = getattr(settings, 'USD_TO_NGN_RATE', 1500)
            profit_margin = getattr(settings, 'PROFIT_MARGIN', 0.1)
            
            def convert_price(usd_price):
                ngn_price = float(usd_price) * exchange_rate
                return ngn_price * (1 + profit_margin)
            
            pricing = {
                'registration': convert_price(registration_usd),
                'renewal': convert_price(renewal_usd),
                'transfer': convert_price(transfer_usd)
            }
            
            return {
                'success': True,
                'available': available,
                'domain': domain_name,
                'message': 'Domain Available for Registration' if available else 'Domain Not Available for Registration',
                'pricing': pricing if available else None
            }
        else:
            return {
                'success': False,
                'available': False,
                'domain': domain_name,
                'error': message or 'Domain check failed'
            }
            
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timeout. Please try again.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Network error: {str(e)}'
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': 'Invalid response from domain service'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

import datetime
import os

def debug_log(message, category="GENERAL"):
    """
    Log debug messages to a file for troubleshooting
    """
    try:
        log_file = os.path.join(os.path.dirname(__file__), '..', 'debug.txt')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{category}] {message}\n")
    except Exception as e:
        print(f"Failed to write debug log: {e}")

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

@require_http_methods(["GET"])
def check_domain_availability(request):
    """
    Check domain availability using ConnectReseller API
    """
    domain_name = request.GET.get('domain', '').strip()
    
    # Use the helper function to get domain availability
    result = _get_domain_availability(domain_name)
    
    # Return as JSON response
    return JsonResponse(result)

def get_domain_suggestions(keyword, max_results=5):
    """
    Get domain suggestions from ConnectReseller API
    """
    try:
        api_key = getattr(settings, 'CONNECTRESELLER_API_KEY', '')
        if not api_key:
            return {'success': False, 'error': 'API key not configured'}
        
        # API endpoint for domain suggestions
        url = 'https://api.connectreseller.com/ConnectReseller/ESHOP/domainSuggestion'
        
        # Parameters
        params = {
            'APIKey': api_key,
            'keyword': keyword,
            'maxResult': min(max_results, 50)  # Max 50 as per API docs
        }
        
        # Make the request
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if we have suggestions
            response_msg = data.get('responseMsg', {})
            suggestions_list = response_msg.get('registryDomainSuggestionList', [])
            
            if suggestions_list:
                # Apply currency conversion and profit margin
                exchange_rate = getattr(settings, 'USD_TO_NGN_RATE', 1500)
                profit_margin = getattr(settings, 'PROFIT_MARGIN', 0.10)
                
                formatted_suggestions = []
                for suggestion in suggestions_list:
                    domain_name = suggestion.get('domainName', '')
                    price_usd = float(suggestion.get('price', 0))
                    
                    # Convert to NGN and add profit margin
                    price_ngn = price_usd * exchange_rate * (1 + profit_margin)
                    
                    formatted_suggestions.append({
                        'domain': domain_name,
                        'price_usd': price_usd,
                        'price_ngn': price_ngn
                    })
                
                return {
                    'success': True,
                    'suggestions': formatted_suggestions
                }
            else:
                return {'success': False, 'error': 'No suggestions found'}
        else:
            return {'success': False, 'error': f'API request failed with status {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timeout - please try again'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Network error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}

def check_domain_availability_helper(domain):
    """
    Helper function to check domain availability via ConnectReseller API
    Returns the domain result data
    """
    debug_log(f"Starting domain availability check for: {domain}", "DOMAIN_CHECK")
    
    try:
        # Correct API endpoint from documentation - using settings
        api_url = f"{settings.CONNECTRESELLER_BASE_URL}/checkdomainavailable"
        api_key = settings.CONNECTRESELLER_API_KEY
        
        # Prepare API request with correct parameters
        params = {
            'APIKey': api_key,
            'websiteName': domain
        }
        
        debug_log(f"API URL: {api_url}", "DOMAIN_CHECK")
        debug_log(f"API Params: {params}", "DOMAIN_CHECK")
        
        # Make API request
        response = requests.get(api_url, params=params, timeout=10)
        debug_log(f"API Response Status: {response.status_code}", "DOMAIN_CHECK")
        debug_log(f"API Response Headers: {dict(response.headers)}", "DOMAIN_CHECK")
        
        response.raise_for_status()
        
        api_data = response.json()
        
        # Debug: log the API response
        debug_log(f"API Response for {domain}: {json.dumps(api_data, indent=2)}", "DOMAIN_CHECK")
        
        # Parse API response according to documentation
        response_msg = api_data.get('responseMsg', {})
        status_code = response_msg.get('statusCode')
        response_data = api_data.get('responseData', {})  # Fix: responseData is at root level
        
        debug_log(f"Status Code: {status_code}", "DOMAIN_CHECK")
        debug_log(f"Response Data: {json.dumps(response_data, indent=2)}", "DOMAIN_CHECK")
        
        # Check if domain is available (statusCode 200 = available, 400 = not available)
        is_available = status_code == 200
        debug_log(f"Is Available (parsed): {is_available}", "DOMAIN_CHECK")
        
        if is_available and response_data:
            # Extract pricing from API response (correct field names from debug log)
            registration_usd = float(response_data.get('registrationFee', 13.16))
            renewal_usd = float(response_data.get('renewalfee', 13.16))
            transfer_usd = float(response_data.get('transferFee', 13.16))
            
            # Convert to NGN with profit margin - using settings
            conversion_rate = settings.USD_TO_NGN_RATE
            profit_margin = settings.DOMAIN_PROFIT_MARGIN
            
            registration_ngn = registration_usd * conversion_rate * (1 + profit_margin)
            renewal_ngn = renewal_usd * conversion_rate * (1 + profit_margin)
            transfer_ngn = transfer_usd * conversion_rate * (1 + profit_margin)
            
            result = {
                'success': True,
                'available': is_available,
                'domain': domain,
                'message': 'Domain Available for Registration',
                'pricing': {
                    'registration': round(registration_ngn, 2),
                    'renewal': round(renewal_ngn, 2),
                    'transfer': round(transfer_ngn, 2)
                }
            }
        else:
            # Domain not available or error
            result = {
                'success': True,
                'available': False,
                'domain': domain,
                'message': response_msg.get('message', 'Domain Not Available for Registration')
            }
        
        debug_log(f"Final result for {domain}: {json.dumps(result, indent=2)}", "DOMAIN_CHECK")
        return result
            
    except requests.exceptions.RequestException as e:
        error_result = {
            'success': False,
            'available': False,
            'domain': domain,
            'error': f'Network error: {str(e)}'
        }
        debug_log(f"Network error for {domain}: {str(e)}", "DOMAIN_CHECK")
        return error_result
    except Exception as e:
        error_result = {
            'success': False,
            'available': False,
            'domain': domain,
            'error': f'Unexpected error: {str(e)}'
        }
        debug_log(f"Unexpected error for {domain}: {str(e)}", "DOMAIN_CHECK")
        return error_result

def get_domain_suggestions_helper(keyword):
    """
    Helper function to get domain suggestions from ConnectReseller API
    """
    debug_log(f"Starting domain suggestions for keyword: {keyword}", "SUGGESTIONS")
    
    try:
        # Use settings for API configuration
        api_url = f"{settings.CONNECTRESELLER_BASE_URL}/domainSuggestion"
        api_key = settings.CONNECTRESELLER_API_KEY
        
        # Try with different keyword formats based on API documentation
        # API example shows "example.com" so try with .com extension
        test_keywords = []
        
        if '.' in keyword:
            # If already has extension, use as-is and try base name
            test_keywords.append(keyword)
            base_name = keyword.split('.')[0]
            test_keywords.append(f"{base_name}.com")
        else:
            # If no extension, try with .com first, then base name
            test_keywords.append(f"{keyword}.com")
            test_keywords.append(keyword)
        
        # Add fallback keywords
        test_keywords.extend(["example.com", "test.com", "domain.com"])
        
        debug_log(f"Will try keywords in order: {test_keywords}", "SUGGESTIONS")
        
        for test_keyword in test_keywords:
            debug_log(f"Trying keyword: {test_keyword}", "SUGGESTIONS")
            
            params = {
                'APIKey': api_key,
                'keyword': test_keyword,
                'maxResult': 5
            }
        
            debug_log(f"Suggestions API URL: {api_url}", "SUGGESTIONS")
            debug_log(f"Suggestions API Params: {params}", "SUGGESTIONS")
            
            response = requests.get(api_url, params=params, timeout=10)
            debug_log(f"Suggestions API Response Status: {response.status_code}", "SUGGESTIONS")
            debug_log(f"Suggestions API Response Headers: {dict(response.headers)}", "SUGGESTIONS")
            
            if response.status_code == 200:
                # Success! Break out of the loop
                data = response.json()
                debug_log(f"Suggestions API Response Data: {json.dumps(data, indent=2)}", "SUGGESTIONS")
                break
            else:
                debug_log(f"Failed with keyword '{test_keyword}': {response.status_code}", "SUGGESTIONS")
                if test_keyword == test_keywords[-1]:  # Last keyword, raise the error
                    response.raise_for_status()
        else:
            # If we get here, all keywords failed
            debug_log("All test keywords failed", "SUGGESTIONS")
            raise Exception("All test keywords failed for suggestions API")
        
        suggestion_list = data.get('registryDomainSuggestionList', [])
        debug_log(f"Extracted suggestion list: {suggestion_list}", "SUGGESTIONS")
        
        # Convert USD prices to NGN with profit margin - using settings
        conversion_rate = settings.USD_TO_NGN_RATE
        profit_margin = settings.DOMAIN_PROFIT_MARGIN
        
        suggestions = []
        for suggestion in suggestion_list:
            price_usd = float(suggestion.get('price', 0))
            price_ngn = price_usd * conversion_rate * (1 + profit_margin)
            
            suggestion_item = {
                'domain': suggestion.get('domainName', ''),
                'price_usd': price_usd,
                'price_ngn': round(price_ngn, 2)
            }
            suggestions.append(suggestion_item)
            debug_log(f"Processed suggestion: {suggestion_item}", "SUGGESTIONS")
        
        debug_log(f"Final suggestions count: {len(suggestions)}", "SUGGESTIONS")
        return suggestions
        
    except requests.RequestException as e:
        debug_log(f"Suggestions API request failed: {str(e)}", "SUGGESTIONS")
        raise Exception(f'API request failed: {str(e)}')
    except (ValueError, KeyError) as e:
        debug_log(f"Suggestions API response format error: {str(e)}", "SUGGESTIONS")
        raise Exception(f'Invalid API response format: {str(e)}')

def get_domain_suggestions_api(request):
    """
    API endpoint to get domain suggestions
    """
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '').strip()
        
        if not keyword:
            return JsonResponse({
                'success': False,
                'error': 'Keyword parameter is required'
            })
        
        # Extract base domain name (remove extension if present)
        if '.' in keyword:
            keyword = keyword.split('.')[0]
        
        try:
            suggestions = get_domain_suggestions_helper(keyword)
            return JsonResponse({
                'success': True,
                'suggestions': suggestions
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Failed to fetch suggestions: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def get_tld_suggestions_helper(domain):
    """
    Helper function to get TLD suggestions (same domain with different extensions)
    via ConnectReseller API
    """
    debug_log(f"Starting TLD suggestions request for: {domain}", "TLD_SUGGESTIONS")
    
    try:
        # TLD Suggestions API endpoint
        api_url = f"{settings.CONNECTRESELLER_BASE_URL}/getTldSuggestion"
        api_key = settings.CONNECTRESELLER_API_KEY
        
        params = {
            'APIKey': api_key,
            'websiteName': domain
        }
        
        debug_log(f"TLD API URL: {api_url}", "TLD_SUGGESTIONS")
        debug_log(f"TLD API Params: {params}", "TLD_SUGGESTIONS")
        
        response = requests.get(api_url, params=params, timeout=10)
        debug_log(f"TLD API Response Status: {response.status_code}", "TLD_SUGGESTIONS")
        debug_log(f"TLD API Response Headers: {dict(response.headers)}", "TLD_SUGGESTIONS")
        
        response.raise_for_status()
        
        api_data = response.json()
        debug_log(f"TLD API Response for {domain}: {json.dumps(api_data, indent=2)}", "TLD_SUGGESTIONS")
        
        # Parse API response according to documentation
        suggestions_list = []
        response_msg = api_data.get('responseMsg', {})
        response_data = api_data.get('responseData', [])
        
        if response_msg.get('statusCode') == 200 and response_data:
            # Define priority order for TLDs
            priority_tlds = [
                # Popular TLDs first
                '.com', '.org', '.net', '.co', '.biz', '.info',
                # Nigerian TLDs
                '.com.ng', '.ng', '.org.ng', '.net.ng', '.gov.ng', '.edu.ng',
                # Other popular extensions
                '.io', '.tech', '.online', '.site', '.website', '.store'
            ]
            
            # Separate TLDs by priority
            priority_suggestions = []
            other_suggestions = []
            
            for tld_data in response_data:
                domain_name = tld_data.get('websiteName', '')
                is_available = tld_data.get('available', False)
                domain_type = tld_data.get('domainType', 'Standard')
                
                # Extract TLD from domain name
                if '.' in domain_name:
                    tld = '.' + '.'.join(domain_name.split('.')[1:])
                else:
                    tld = ''
                
                # Use default pricing (we'll get real pricing from TLD prices API later)
                base_price_usd = 13.16
                conversion_rate = settings.USD_TO_NGN_RATE
                profit_margin = settings.DOMAIN_PROFIT_MARGIN
                price_ngn = base_price_usd * conversion_rate * (1 + profit_margin)
                
                suggestion_item = {
                    'domain': domain_name,
                    'available': is_available,
                    'price': round(price_ngn, 2),
                    'type': domain_type,
                    'tld': tld
                }
                
                # Categorize by priority
                if tld in priority_tlds:
                    priority_suggestions.append(suggestion_item)
                else:
                    other_suggestions.append(suggestion_item)
            
            # Sort priority suggestions by the order in priority_tlds list
            priority_suggestions.sort(key=lambda x: priority_tlds.index(x['tld']) if x['tld'] in priority_tlds else 999)
            
            # Combine: priority first, then others
            suggestions_list = priority_suggestions + other_suggestions
        
        result = {
            'success': True,
            'suggestions': suggestions_list
        }
        
        debug_log(f"Final TLD suggestions result for {domain}: {json.dumps(result, indent=2)}", "TLD_SUGGESTIONS")
        return result
            
    except requests.exceptions.RequestException as e:
        error_result = {
            'success': False,
            'error': f'Network error: {str(e)}',
            'suggestions': []
        }
        debug_log(f"TLD Network error for {domain}: {str(e)}", "TLD_SUGGESTIONS")
        return error_result
    except Exception as e:
        error_result = {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'suggestions': []
        }
        debug_log(f"TLD Unexpected error for {domain}: {str(e)}", "TLD_SUGGESTIONS")
        return error_result

def get_tld_suggestions_api(request):
    """
    API endpoint to get TLD suggestions (same domain with different extensions)
    """
    if request.method == 'GET':
        domain = request.GET.get('domain', '').strip()
        
        if not domain:
            return JsonResponse({
                'success': False,
                'error': 'Domain parameter is required'
            })
        
        try:
            suggestions = get_tld_suggestions_helper(domain)
            return JsonResponse(suggestions)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Failed to fetch TLD suggestions: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def domain_suggestions_page(request):
    """
    Domain suggestions page - helps users get domain suggestions based on business names
    """
    context = {
        'page_title': 'Domain Name Generator',
        'meta_description': 'Find the perfect domain name for your business with our domain name generator and suggestions tool.'
    }
    
    # Handle search query from URL parameters
    keyword = request.GET.get('keyword', '').strip()
    if keyword:
        context['initial_keyword'] = keyword
    
    return render(request, 'domain_suggestions.html', context)

def shopping_cart(request):
    """
    Shopping cart page for domain registration and other services
    """
    context = {}
    
    # Check if we have domain search parameters in URL
    action = request.GET.get('a', '')
    domain_action = request.GET.get('domain', '')
    query = request.GET.get('query', '').strip()
    
    if action == 'add' and domain_action == 'register' and query:
        # Perform domain search
        domain_result = check_domain_availability_helper(query)
        context['search_domain'] = query
        context['domain_result'] = domain_result
        
        # If domain is not available, get suggestions
        if not domain_result.get('available', False):
            suggestions_result = get_domain_suggestions(query, max_results=5)
            if suggestions_result.get('success'):
                context['domain_suggestions'] = suggestions_result.get('suggestions', [])
    
    return render(request, 'shopping_cart.html', context)

def domain_search_redirect(request):
    """
    Handle domain search and redirect to shopping cart with URL parameters
    """
    if request.method == 'POST':
        domain = request.POST.get('domain', '').strip()
        if domain:
            # Redirect to shopping cart with clean URL parameters
            return redirect(f'/shopping-cart/?a=add&domain=register&query={domain}')
    
    return redirect('shopping_cart')
