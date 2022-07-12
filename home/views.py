# importing from python library
import uuid
import json
import requests

# importing from django library
from django.shortcuts import redirect, render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.auth.models import User

from . forms import *
from . models import *



# Create your views here.
def index(request):
    trending = Product.objects.filter(trending=True)

    context = {
        'trending':trending,
    }
    return render(request, 'index.html', context)
    # return HttpResponse('hi im frank')




def contact(request):
    form = ContactForm()#instatiate the contactform for a GET request
    if request.method == 'POST': #make a POST REQUEST
        form = ContactForm(request.POST)    #instatiate the contactform for a POST request
        if form.is_valid():#Django will validate the form
            form.save()#if validate, save the data to the DB
            messages.success(request, 'I have received your message.')
            return redirect('index')#return to index once the post action is carried out
    return render(request, 'index.html')
    # return HttpResponse('Contact done')


def products(request):
    product = Product.objects.all()

    context = {
        'product':product,
    }

    return render(request, 'products.html',context)


def details(request, id):
    detail = Product.objects.get(pk=id)
    context = {
        'detail':detail,
    }
    return render(request, 'details.html',context)  


# authenticaion
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        usernamee = request.POST['username']
        passwordd = request.POST['password']
        user = authenticate(request, username=usernamee, password=passwordd)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signin successful!')
            return redirect('index')
        else:
            messages.error(request, 'Username/Password incorrect. Kindly supply valid details')
            return redirect('signin')
    return render(request, 'signin.html')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            newprofile = Profile(user = newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.state = state
            newprofile.save()
            login(request, newuser)
            messages.success(request, 'Signup Successful!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')

# authentication done      

# profile 

@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user_id = request.user.id)

    context = {
         'profile':profile,
    }

    return render(request, 'profile.html', context)     


@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    update = ProfileUpdate(instance = request.user.profile)#instantiate the form for a GET request along with the user's details
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.FILES, instance= request.user.profile)#instantiate the form for a POST request along with the user's details
        if update.is_valid():
            update.save()
            messages.success(request, 'profile update successful!')
            return redirect('profile')
        else:
            messages.error(request, update.errors)   
            return redirect('profile_update') 

    context = {
        'profile':profile,
        'update':update,
    }

    return render(request, 'profile_update.html', context) 
    # profile done 


@login_required(login_url='signin')
def password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    # form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(request.user)
        # form = PasswordChangeForm(request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password change successfull')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')    

    context = {
        'form':form,
        'profile':profile,
    }       
    return render(request, 'password.html', context) 
    # profile done 


 # shopcart
def shopcart(request):
    if request.method =='POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product_id']
        item = Product.objects.get(pk= item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        cart_no = order_num.id

        cart = Shopcart.objects.filter(user__username = request.user.username, paid= False)
        if cart:
            basket = Shopcart.objects.filter(products= item.id, user__username=request.user.username).first()
            if basket:
                basket.quantity +=quant
                basket.amount = basket.price * quant
                basket.save()
                messages.success(request, 'Item added to cart.')
                return redirect('products')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.products = item
                newitem.quantity = quant
                # newitem.name_id = item.name
                newitem.price = item.price
                newitem.amount = item.price * quant
                newitem.order_no = cart_no
                newitem.paid = False  
                newitem.save()
                messages.success(request, 'Item added to cart.')
                return redirect('products')  
        else:
            newcart = Shopcart()
            newcart.user = request.user
            newcart.products = item
            newcart.quantity = quant
            # newcart.name_id = item.name  
            newcart.price = item.price
            newcart.amount = item.price * quant
            newcart.order_no = cart_no
            newcart.paid = False  
            newcart.save()        
            messages.success(request, 'item added to shopcart.')
            return redirect('products')
    
    return redirect('products')

def displaycart(request):
    trolley = Shopcart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for item in trolley:
        subtotal += item.price * item.quantity

    vat = 0.075 * subtotal

    total = vat + subtotal    
    
    context ={
        'trolley':trolley,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }

    return render(request, 'displaycart.html', context)   

def deleteitem(request):
    item_id = request.POST['item_id']  
    item_delete = Shopcart.objects.get(pk=item_id)
    item_delete.delete()
    messages.success(request, 'item deleted successfully')
    return redirect('displaycart')   

def increase(request):
    if request.method == 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity = the_quant
        modify.amount = modify.price * modify.quantity
        modify.save()
    return redirect('displaycart')   

# shopcart done


#checkout using class based view and axios get request     
class Checkout1View(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid=False)
        subtotal = 0
        vat = 0
        total = 0

        for item in summary:
            subtotal += item.price * item.quantity

        vat = 0.075 * subtotal

        total = vat + subtotal   
        context ={
            'summary':summary,
            'total':total,
        }
        return render(request, 'checkout1.html',context)
#checkout using class based view and axios get request done

def pay(request):
    if request.method == 'POST':
        # collecting data to send out to paystack
        api_key = 'sk_test_43762140e809dbc5ffee4d9c1e84d8c72afd6b9d'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://18.234.99.10/callback'
        user = User.objects.get(username = request.user.username)
        email = user.email
        total = float(request.POST['total']) * 100
        cart_no = user.profile.id
        transac_code = str(uuid.uuid4())
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':transac_code,'email':email, 'amount':int(total), 'order_number':cart_no, 'callback_url':cburl, 'currency': 'NGN'}
        # print('TESTING', data)
        # integrating to paystack
        try:
            r = requests.post(curl, headers= headers, json= data)
        except Exception:
            messages.error(request, 'Network busy, refresh and try again')
        else:
            transback = json.loads(r.text)
            # rdurl = transback['data']['authorization_url']
            rdurl = transback['data']['authorization_url']
            return redirect(rdurl)
        return redirect('displaycart')

def callback(request):

    context ={
        
    }

    
    return render(request, 'callback.html', context)



