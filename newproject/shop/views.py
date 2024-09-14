from django.shortcuts import render, redirect, get_object_or_404
from .models import  Product,Customer,Cart
from .forms import ProductForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.conf import settings

# View for displaying categories and products
def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', { 'products': products})

def about(request):
    return render(request, 'shop/about.html')

def contact_us(request):
    return render(request, 'shop/contact_us.html')

def showProduct(request,prodType,prodId):
    validProds=['seeds','machines','fertilizer']
    prod=Product.objects.filter(category=prodType,id=prodId)[0]
    print(prod)
    if prodType in validProds and prod:
        prodArr=Product.objects.filter(Q(category=prodType) & (~Q(id=prodId)) )[:3]
        print('ok ok ')
        return render(request,'shop/product.html',{'prod':prod,'prodArr':prodArr})
    print(prodType)
    print(prodId)
    return render(request,'shop/product.html')

# code to get the products based on category -> seed, machinery, fertilizer
def listProduct(request,prodType):
    validProds=['seeds','machines','fertilizer']
    if prodType not in validProds:
        return render(request,'shop/404.html')
    prodArr= Product.objects.filter(category=prodType)
    print(prodArr)
    for i in prodArr:
        print(i.image)
    #count=[i for i in range(20)]
    capitalProd=prodType.capitalize()
    return  render(request,'shop/categoryProd.html',{'prodArr':prodArr,'prodType':capitalProd})

def login_user(request):
    if request.method=='POST':
        print('trying to get env variable')
        print(settings.ADMIN_EMAIL)
        print('inside login_user')
        print(request.POST)
        email=request.POST.get('cemail')
        passwd=request.POST.get('password')
        print(email,passwd)
        # Checking the password
        is_valid = check_password(passwd, settings.ADMIN_PASS)
        print('is ADMIN password hash valid')
        print(is_valid)  # Output: True
        if email==settings.ADMIN_EMAIL and is_valid:
            request.session['adminEmail']=email
            request.session['adminId']=settings.ADMIN_ID
            return redirect('adminHome')
        else:
            user=Customer.objects.filter(email=email).first()
            print(user)
            if not user:
                print('No such user')
                return render(request,'shop/login.html',{'msg':'No such user exist'})
            elif user.check_password(passwd):
                print('success')
                request.session['userId']=user.id
                request.session['userEmail']=user.email
                return redirect('home')
            else:
                print('inivalid pass')
                return render(request,'shop/login.html',{'msg':"Invalid Password"})
    return render(request,'shop/login.html')

def register_user(request):
    if request.method=='POST':
        print('inside register_user')
        print(request.POST)
        name=request.POST.get('cname')
        email=request.POST.get('cemail')
        passwd=request.POST.get('password')
        try:
            customer=Customer(name=name,email=email,password=passwd)
            #if customer:
                #customer.set_password(passwd)
            customer.save()
            print(customer.id)
            request.session['userId']=customer.id
            request.session['userEmail']=customer.email
            print(customer)
            return redirect('home')
        except Exception:
            print('exception')
            return render(request,'shop/register.html')        
    return render(request,'shop/register.html')

def logout_view(request):
    logout(request)
    return redirect('home')

from django.http import JsonResponse
import json
def add_to_cart(request):#just add to cart table no need to navigate to cart page
    #here we also need to check if user is loggedIn , else navigate to login page
    if request.session.get('userId') and request.session.get('userEmail'):
        userId=request.session.get('userId')
        if(request.method=='POST'):
            data = json.loads(request.body)
            #print(data)
            #print('Inside add_to_cart')
            #print(data['prodId'])
            #print(data['prodCount'])
            product=Product.objects.get(id=data['prodId']) 
            user=Customer.objects.get(id=userId)
            cartInfo=Cart(prodId=product,userId=user,prodCount=data['prodCount'])
            cartInfo.save()
            print(cartInfo)
            return JsonResponse({'status':200,'msg':'Success'})
    else:
        return JsonResponse({'status':400,'msg':'Please Login to add items to cart'})


#for fetilizer -> 5% gst, +60/kg
#for seeds -> 0% gst, +30/kg
# for machines -> 18% gst, + max(₹100 /kg or 5% of price)
def calculatePrice(category,price,quantity):
    gst=0
    shipPrice=0
    if category=='seeds':
        shipPrice=30*quantity
    elif category=='fertilizer':
        gst=5*price*quantity/100
        shipPrice=min(50*quantity,10*price*quantity/100)
    else:
        gst=18*price*quantity/100
        shipPrice=max(100*quantity,5*price*quantity/100)
    return gst,shipPrice

def buy_product(request, product_id):
    if request.session.get('userId') and request.session.get('userEmail'):
        if request.method == 'POST':
            print(product_id)
            product = Product.objects.filter(id=product_id).first()
            quantity=int(request.POST.get('quantity'))
            if product:
                print(product)
                print(product.price)
                actualPrice=product.price*int(quantity)
                gst,shipPrice=calculatePrice(product.category,product.price,quantity)
                total=gst+shipPrice+actualPrice
                prices={
                    'gst':gst,
                    'shipPrice':shipPrice,
                    'total':total
                }
                return render(request,'shop/checkout.html', {"product":product,'quantity':quantity,'cartTotal':total,'prices':prices,'single':True})
        return render(request,'shop/home.html')
    else:
        return redirect('login')

def showCart(request):
    print('inside cart --------------------------')
    if request.session.get('userId') and request.session.get('userEmail'):
        #print(request.session.get('userId'))
        #print(request.session.get('userEmail'))
        userId=request.session.get('userId')
        #print(type(userId))
        #here write logic to get data from cart and display in pager
        userData=Customer.objects.get(id=userId)
        #print(userData)
        cartData=False
        cartData=Cart.objects.filter(userId=userData.id)
        #print('cartData is ')
        #print(cartData)
        total=0
        for i in cartData:
            i.subTotal=i.prodId.price*i.prodCount
            total+=i.subTotal
            print(i.prodId.name)
        
        return render(request,'shop/cart.html',{'cartData':cartData,'total':total})
    else:
        return redirect('login')
    
def removeCart(request,cart_id):
    if request.session.get('userId') and request.session.get('userEmail'):
        cart=Cart.objects.filter(id=cart_id)
        if cart:
            print(cart)
            cart.delete()
        return redirect('cart')

def cartToCheckout(request):
    if request.session.get('userId') and request.session.get('userEmail'):
        pass


def showCheckout(request):
    if request.session.get('userId') and request.session.get('userEmail'):
        user=Customer.objects.filter(id=request.session.get('userId'))
        print(user)
        cartDetail=Cart.objects.filter(userId=user[0])
        cartTotal=0
        prodArr=[]
        print(cartDetail)
        for i in cartDetail:
            print(i)
            prod=i.prodId
            qty=i.prodCount
            print(qty)
            actualPrice=prod.price*int(qty)
            gst,shipPrice=calculatePrice(prod.category,prod.price,qty)
            total=gst+shipPrice+actualPrice
            cartTotal+=total
            prodArr.append({'prod':prod,'qty':qty,'gst':gst,'shipPrice':shipPrice,'total':total})
        print(prodArr)
        return render(request,'shop/checkout.html', {'cartTotal':cartTotal, 'prodArr':prodArr })
    else:
        return redirect('login')


def adminHome(request):
    if request.session.get('adminId') and request.session.get('adminEmail'):
        prodList=Product.objects.all()
        return render(request,'shop/adminHome.html',{'prodList':prodList})
    else:
        return redirect('home')

def add_product(request):
    if request.session.get('adminId') and request.session.get('adminEmail'):
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = ProductForm()
        return render(request, 'shop/add_product.html', {'form': form})
    else:
        return redirect('home')