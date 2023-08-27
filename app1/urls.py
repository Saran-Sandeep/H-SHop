"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app1 import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('login/', views.handle_login, name="login"),
    path('signup/', views.handle_signup, name="signup"),
    path('logout/', views.handle_logout, name="logout" ),
    path('explore/', views.handle_explore, name="explore" ),
    path('cart/', views.handle_cart, name="cart" ),
    path('checkout/', views.handle_checkout, name="checkout" ),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('update_item/', views.handle_update_item, name="update_item"),
]
