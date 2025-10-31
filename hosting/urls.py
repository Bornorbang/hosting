"""
URL configuration for hosting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('web-hosting/', views.web_hosting, name='web_hosting'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    # Support Pages
    path('contact-us/', views.contact_us, name='contact_us'),
    path('help-center/', views.help_center, name='help_center'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    
    # Company Pages
    path('about-us/', views.about_us, name='about_us'),
    path('blog/', views.blog, name='blog'),
    path('careers/', views.careers, name='careers'),
    
    # Legal Pages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
