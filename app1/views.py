from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from app1.models import *
from math import ceil
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def home(request) :
    allProds = []
    catprods = Product.objects.values('category' , 'id')
    cats = { item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        # nSlides = n // 4 + ceil((n / 4) - (n//4))
        nSlides = 1
        allProds. append([prod, range(1, nSlides), nSlides])
        print(allProds)
    params = { 'allProds' : allProds }
    return render(request, "home.html" , params)

def handle_login(request):

    if(request.method=="POST"):
        uname = request.POST['Inputusername']
        pass1 = request.POST['pass1']
        user = authenticate(username=uname, password=pass1)
    
        if user is not None:
            login(request, user)
            return redirect("/home/")
        else:
            return render(request, 'login.html', {'invalid_cred' : True})
    return render(request, 'login.html')


def handle_signup(request):

    if(request.method=="POST"):
        uname = request.POST['username']
        emailid = request.POST['InputEmail1']
        pass1 = request.POST['InputPassword1']
        pass2 = request.POST['InputPassword2']

        if(pass1!=pass2):
            return render(request, 'signup.html', {'passmm' : True})

        try:
            if(User.objects.get(username=uname)):
                return render(request, 'signup.html', {'alreadyexists' : True})
        except Exception as e:
            pass

        user = User.objects.create_user(uname, emailid, pass1)       
        user.is_active = False
        user.save() 

        email_sub = "Activate ur Account"
        message = render_to_string('activate.html', {
            'user' : user,
            'domain': '127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user),
        })

        email_msg = EmailMessage(
            email_sub,
            message,
            settings.EMAIL_HOST_USER,
            [emailid],
        )
        email_msg.send()
        
        return render(request, 'login.html', {'mailsent' : True})
    return render(request, 'signup.html')

class ActivateAccountView(View): 
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        return render(request, 'activatefail.html')

def handle_logout(request):
    logout(request)
    return render(request, 'home.html', {'logout_success' : True})

def handle_cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def handle_checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def handle_explore(request):

    products = Product.objects.all()
    context = {'products':products, 'cartItems':products}

    return render(request, 'explore.html', context)

def handle_update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    # print('Action:', action)
    # print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

