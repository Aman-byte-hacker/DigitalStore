from django.shortcuts import render,redirect
from .models import Payment, Product,Category, Userproduct
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def index(request):
    product = None
    category = Category.objects.all().order_by('id')
    categoryid = request.GET.get('category')
    print(categoryid)
    if categoryid:
        product = Product.get_allproducts_by_category(categoryid)
    else:
        product = Product.objects.filter(is_available=True).order_by('id')
    context = {
        'products':product,
        'categories':category
    }
    return render(request,"index.html",context)

def see(request,product_id):
    product = Product.objects.filter(id=product_id)
    context={
        'products':product
    } 
    return render(request,"see.html",context)   

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Having an Account")
        elif User.objects.filter(username=username).exists():
            messages.error(request,"Username Taken")
        else:
            if password1 == password2:
                messages.success(request,"You are registered Successfully...")
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.first_name = first_name
                user.last_name = last_name
                return redirect("/login")
            else:
                messages.error(request,"password1 and password2 are not matching...")
                            
    return render(request,"register.html")    


def order(request):
    product = Userproduct.objects.all()
    context={
        'products' : product
    }
    return render(request,"order.html",context)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
            messages.success(request,"Logged In Successfully")
        else:
            messages.error(request,"Invalid Credentials")    
    return render(request,"login.html")        

def logout(request):
    auth.logout(request)
    return redirect("/")
    messages.success(request,"Successfully Logged Out")    

import razorpay
client = razorpay.Client(auth=("rzp_test_LtPqXSjfBHD1BO", "GcIcHev1lYLoUc4skQwqplO2"))

@login_required
def payment(request,product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('/login')    
    product = Product.objects.get(id=product_id)
    order_amount = product.price * 100
    order_currency = 'INR'
    order_receipt = 'order_rcptid_{product.id}_{user.id}'
    data = {
        'amount' : order_amount,
        'currency' : order_currency,
        'receipt' : order_receipt
    }
    order = client.order.create(data=data)
    payment = Payment(user=user,product=product,status='FAIL',order_id=order.get('id'))
    payment.save()
    print(order)
    context={
        'product':product,
        'order': order
    }

    return render(request,"payment.html",context) 

@csrf_exempt
def paymentverify(request):
    if request.method == "POST":
        print(request.POST)
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id = razorpay_order_id)
        payment.status = "SUCCESS"
        payment.payment_id = razorpay_payment_id
        payment.save()

        user_product = Userproduct(user = payment.user,payment=payment,product=payment.product)
        user_product.save()
        return redirect('/orders')