from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
#from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from  admin1 . models import categories,products,Address,Order,myuser,Coupon,Referal
from admin1 . models import cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from decimal import Decimal
#from decimal import *
from django.contrib.auth.hashers import check_password
import random
from twilio.rest import Client
from django.core.files import File
#from django.views.decorators.cache import cache_page
from django.core.cache import cache

#from urllib import request
# Create your views here.
def index(request):
    return render(request,"index.html")


def login(request):

    #if request.session.has_key('key'):
     #   return render(request,'login.html')

    if request.method== 'POST':
        print("haii")
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.get(username=username)

        if user.is_active == True:
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                request.session['key']='high'
                return JsonResponse('true',safe=False)
            
            else:   
                return JsonResponse('false', safe=False)

        else:
            return JsonResponse('block',safe=False)        
            
    else:    
        return render(request,'login.html')
    
    

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first1']
        last_name = request.POST['last1']
        username = request.POST['user1']
        mobile = request.POST['mobile1']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        email =request.POST['email1']
            
        if password1==password2:
            if User.objects.filter(username=username).exists():
                return JsonResponse('false3',safe=False)
                   
            elif User.objects.filter(email=email).exists():
                return JsonResponse('false4',safe=False)
            elif myuser.objects.filter(mobile_number=mobile):    
                return JsonResponse('false5',safe=False)       

            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,)
                myuse= myuser.objects.create(user=user,mobile_number=mobile)
                user.save()
                myuse.save()

                
                return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false4', safe=False)
            #return redirect('register')    
            
    else:    
        return render(request,'register.html')

def otp_request(request):

    if request.method== 'POST':
        mobile=request.POST['mobile']
        if myuser.objects.filter(mobile_number=mobile).exists():
            request.session['mobile']=mobile
            random_num=random.randint(1000,9999)
            global Otp
            Otp=random_num

            account_sid='AC5be1f48670a3e66b015732ca4d5dc8f8'
            auth_token='febf45e04f687647be9bd1d1a8e3df5e'
            client=Client(account_sid,auth_token)

            message=client.messages.create(
                body=f"your otp for login is {Otp}",
                from_='+14439988833',
                to=f'+916282117443' 
            )

            return JsonResponse('true',safe=False)
        else:
            return JsonResponse('false',safe=False)    

    else:
        return render(request,"otplogin.html")

def otp_validate(request):
    if request.method =='POST':
        mobile=request.session['mobile']
        users=myuser.objects.get(mobile_number=mobile)
        user1 = users.user
        otp_entered = request.POST['otp1']

        global Otp
        print(otp_entered,'>>>>>>>>>>>>>>')
        print(mobile)
        print(otp_entered)
        print(type(otp_entered),type(Otp))
        if Otp == int(otp_entered) :
            auth.login(request,user1)
            return JsonResponse('true',safe=False)

    else:
        return render(request,'otp_validate.html')

def referal_register(request,id):
    users = User.objects.get(id=id)
    
    if request.method == 'POST':
        first_name = request.POST['first1']
        last_name = request.POST['last1']
        username = request.POST['user1']
        mobile = request.POST['mobile1']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        email =request.POST['email1']
            
        if password1==password2:
            if User.objects.filter(username=username).exists():
                return JsonResponse('false3',safe=False)
                   
            elif User.objects.filter(email=email).exists():
                return JsonResponse('false4',safe=False)
            elif myuser.objects.filter(mobile_number=mobile):    
                return JsonResponse('false5',safe=False)       

            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,)
                myuse= myuser.objects.create(user=user,mobile_number=mobile)

                user.save()
                myuse.save()

                random_num=random.randint(1000,9999)
                Referal.objects.create(referal_code=random_num, offer='10', user=user)
                print(user)

                random_num=random.randint(1000,9999)
                Referal.objects.create(referal_code=random_num, offer='10',user=users)
                return JsonResponse('true', safe=False)
        else:
            return JsonResponse('false4', safe=False)
            #return redirect('register')    
            
    else:    
        return render(request,'referal_register.html',{'user':users})



def orderstatus(request):
#if request.session.has_key("setkey"):
    if request.method =='POST':
        orderid = request.POST['orderid']
        order =Order.objects.get(id=orderid)

        if request.POST ['clicked'] == 'shipped':
            print("hai")
            order.status = 'shipped'
            order.save()
        elif requeset.POST['clicked'] == 'Delivered':
            print("hoiii")
            order.status = 'delivered'   
            order.save()
        return JsonResponse('true',safe=False)    
    else:
        return redirect(index)

def addtocart(request,pk):
    if request.user.is_authenticated:
        users = request.user
        carts = products.objects.get(id=pk)

        mycart, created = cart.objects.get_or_create(user=users,product=carts)
        mycart.quantity = 1
        print("cartadded")
        mycart.save()
        return redirect(index)
    else:
        return redirect(index)

@login_required
def cartview(request):

    users = request.user.id
    cart1 = cart.objects.filter(user_id=users)

    total = 0
    for carts in cart1:
        quantity = carts.quantity
        if carts.product.category.discount==0:
            price=carts.product.price
        else:
            price=carts.product.discountprice
        total = total + (price * quantity)
        carts.total = (price * quantity)
        request.session['total'] = float(total)

    context = {
        'carts': cart1,
        'total': total
    }
    return render(request, 'viewcart.html', context)



def removecart(request,pk):
    product = cart.objects.get(id=pk)
    product.delete()
    return redirect(cartview)


@csrf_exempt
def add_quantity(request, cart_id):
    cart1 = cart.objects.get(id=cart_id)
    carts = cart.objects.filter(user=request.user)
    print(cart.quantity)
    if cart1.quantity > 19:
        return JsonResponse('false', safe=False)
    else:
        cart1.quantity += 1
        cart1.save()
    if cart1.product.discountprice == 0:
        item_total = cart1.quantity * cart1.product.price
    else:
        item_total = cart1.quantity * cart1.product.discountprice

    total = 0
    for x in carts:
        if cart1.product.discountprice == 0:
            total = total + x.quantity * x.product.price
        else:
            total = total + x.quantity * x.product.discountprice

    data = {
        'quantity': cart1.quantity,
        'item_total': item_total,
        'total': total
    }
    return JsonResponse(data)


@csrf_exempt
def reduce_quantity(request, cart_id):
    cart1 = cart.objects.get(id=cart_id)
    print(cart.quantity)
    if cart1.quantity < 2:
        cart1.delete()
    else:
        cart1.quantity -= 1
        cart1.save()
    if cart1.product.discountprice == 0:    
        item_total = cart1.quantity * cart1.product.price
    else:
        item_total = cart1.quantity * cart1.product.discountprice        
    carts = cart.objects.filter(user_id=request.user)
    total = 0
    for x in carts:
        total = total + x.product.price * x.quantity
    data = {
        'quantity': cart1.quantity,
        'item_total': item_total,
        'total': total,
        # 'carts': serializers.serialize('json', carts)
    }
    return JsonResponse(data)


def checkout(request):
    if request.user.is_authenticated:
        users=request.user
        address1 = Address.objects.filter(user_id=users)
        users = request.user.id
        cart1 = cart.objects.filter(user_id=users)
        total = 0
        for carts in cart1:
            if carts.product.discountprice == 0:
                total = total + (carts.product.price * carts.quantity)
            else:
                total = total + (carts.product.discountprice * carts.quantity)

        if request.method == 'POST':
            print("hai")
            coupon_code = request.POST['coupon']
            user=request.user
            carts=cart.objects.filter(user=user)
            if Coupon.objects.filter(coupon_code=coupon_code):
                coupon=Coupon.objects.get(coupon_code=coupon_code)
                print(total)
                coupdiscount= total * coupon.offer/100
                total = total - coupdiscount
                
                return render(request,"checkout.html",{'address':address1,'total':total})
        else:  
            return render(request,"checkout.html",{'address':address1,'total':total})
    else:
        return redirect(login)    

def addaddress(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            housename = request.POST['housename']
            town = request.POST['town']
            district = request.POST['district']
            state = request.POST['state']
            pincode = request.POST['pincode']
            mobile = request.POST['mobile']
            users = request.user

            address=Address.objects.create(user=users,house_name=housename,town=town,district=district,state=state,pin_code=pincode,mobile=mobile)
            print("address created")
            return redirect(checkout)

        else:
            return render(request,"addaddress.html")    

@csrf_exempt
def selectaddress(request, add_id):
    if request.user.is_authenticated:
        request.session['add']=add_id
        return JsonResponse('true',safe=False)
        #address1=Address.objects.filter(user=request.user,id=add_id)
        
    else:
        return redirect(index)    

def addressdelete(request,pk):
    add=Address.objects.get(id=pk)
    add.delete()
    return redirect(checkout)

def orderpayment(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            value=request.GET['value']
            if value =='cod':
                print("haiii")
                return JsonResponse('cod',safe=False)
            elif value =='paypal':
                return JsonResponse('paypal',safe=False)
            elif value =='razorpay':
                return JsonResponse('razorpay',safe=False)    
    else:
        return redirect(index)
def cod(request):
    if request.user.is_authenticated:
        user=request.user
        address_id=request.session['add']
        address=Address.objects.get(id=address_id)
        carts=cart.objects.filter(user=user)
        for i in carts:
            if i.product.discountprice == 0:
                price=i.quantity * i.product.price
                Order.objects.create(user=i.user,products=i.product,address=address,status='Ordered',payment_method='COD',count=i.quantity,price=price)
                cart_del=cart.objects.get(id=i.id)
                cart_del.delete()
            else:
                price=i.quantity * i.product.discountprice
                Order.objects.create(user=i.user,products=i.product,address=address,status='Ordered',payment_method='COD',count=i.quantity,price=price)
                cart_del=cart.objects.get(id=i.id)
                cart_del.delete()

        print("order created")

        return render(request,'cod.html')
    else:
        return redirect(index)

def paypal(request):
    if request.user.is_authenticated:
        user=request.user
        carts=cart.objects.filter(user=user)
       
        total=0
        for i in carts:
            if i.product.discountprice == 0:
                total = total + i.quantity * i.product.price  
            else:
                total = total + i.quantity * i.product.discountprice

        return render(request,"paypal.html",{'totals':total})

def paypalsuccess(request):
    if request.user.is_authenticated:
        user=request.user
        address_id=request.session['add']
        address=Address.objects.get(id=address_id)
        carts=cart.objects.filter(user=user)
        for i in carts:
            if i.product.discountprice == 0:
                price=i.quantity * i.product.price
                Order.objects.create(user=i.user,products=i.product,address=address,status="Ordered",payment_method='PayPal',count=i.quantity,price=price)
                print("order created")
                cart_del=cart.objects.get(id=i.id)
                cart_del.delete()
            else:
                price = total + i.quantity * i.product.discountprice
                Order.objects.create(user=i.user,products=i.product,address=address,status="Ordered",payment_method='PayPal',count=i.quantity,price=price)
                print("order created")
                cart_del=cart.objects.get(id=i.id)
                cart_del.delete()

        return render(request,"paypalsuccess.html")

def razorpay(request):
    if request.user.is_authenticated:
        user=request.user
        carts=cart.objects.filter(user=user)

        total=0
        for i in carts:
            if i.product.discountprice == 0:
                total = total + i.quantity * i.product.price 

            else:
                total = total + i.quantity * i.product.discountprice

        return render(request,"razorpay.html",{'totals':total,'cart':carts})
    else:
        return redirect(index)

@csrf_exempt       
def razorpaysuccess(request):
    if request.method == 'POST':
        user=request.user
        address_id=request.session['add']
        address=Address.objects.get(id=address_id)
        carts=cart.objects.filter(user=user)

        for i in carts:
            if i.product.discountprice == 0:
                price=i.quantity * i.product.price
                Order.objects.create(user=i.user,products=i.product,address=address,status="Ordered",payment_method='RazorPay',count=i.quantity,price=price)
                i.delete()
            else:
                price=i.quantity * i.product.discountprice
                Order.objects.create(user=i.user,products=i.product,address=address,status="Ordered",payment_method='RazorPay',count=i.quantity,price=price)
                i.delete()

        return redirect(cartview)

    else:
        return redirect(razorpay)
    

def razorsuccess(request):
    if request.user.is_authenticated:
        user=request.user
        address_id=request.session['add']
        address=Address.objects.get(id=address_id)
        carts=cart.objects.filter(user=user)

        return render(request,"razorpay.html")


def productdetails(request,pk):
    product=products.objects.get(id=pk)
    return render(request,"productdetails.html",{'products':product})


def userprofile(request):
    if request.user.is_authenticated:
        #user=User.objects.all()
        
        #referal=Referal.objects.get(user=request.user)
        
        host = request.get_host()
        print(host)
        address1=Address.objects.filter(user=request.user)
        myuse=myuser.objects.get(user=request.user)
        return render(request,"userprofile.html",{'address':address1,'myuser':myuse,'host':host})
    else:
        return redirect(index)
def addimage(request):
    if request.user.is_authenticated:
        users=request.user
        image1 = request.FILES.get('imageupload')
        print(image1)
        my=myuser.objects.get(user=users)
        my.image=image1
        my.save()
        print("created")
        return JsonResponse('true',safe=False)

    else:
        return redirect(userprofile)

def userorders(request):
    if request.user.is_authenticated:
        orders= Order.objects.filter(user=request.user)
        return render(request,"userorders.html",{'orders':orders})

def order_cancel(request,pk):
    orders=Order.objects.get(id=pk)
    orders.status = 'user canceled order'
    orders.save()

    return redirect(userorders)




def editprofile(request,pk):
    if request.user.is_authenticated:
    
        if request.method == 'POST':
            user=request.user
            id=request.user.id
            user.first_name = request.POST['first1']
            user.last_name = request.POST['last1']
            user.username = request.POST['user1']
            user.email =request.POST['email1']
                
            if User.objects.filter(first_name=user.first_name).exclude(id=pk).exists():
                return JsonResponse('false1',safe=False)
            elif User.objects.filter(last_name=user.last_name).exclude(id=pk).exists():
                return JsonResponse('false2',safe=False)
            elif User.objects.filter(username=user.username).exclude(id=pk).exists():
                return JsonResponse('false3',safe=False)
            elif User.objects.filter(email=user.email).exclude(id=pk).exists():
                return JsonResponse('false4',safe=False)

            else:
                user= User.objects.filter(id=id).update(first_name=first_name,last_name=last_name,username=username,email=email)
                print("user updated")
                return JsonResponse('true',safe=False)
                
        else:
            users=User.objects.get(id=pk)    
            return render(request,"editprofile.html",{'user':users}) 
    else:
        return redirect(index)

def editpassword(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            current_entered=request.POST['passwords']
            current_password=request.user.password
            new_password1=request.POST['password1']
            check = check_password(current_entered,current_password)
            if check == True:
                user1 = User.objects.get(id=request.user.id)
                user1.set_password(new_password1)
                user1.save()
                return JsonResponse('true',safe=False)


        else:
            return render(request,'editprofile.html')    

    else:
        return redirect('index')


def logout(request):
    request.session.flush()
    return redirect('/')

def index(request):
    product=products.objects.all()
    category=categories.objects.all

    return render(request,"index.html", {'products':product,'categories':category})


def product_category(request,pk):
    if request.user.is_authenticated:
        category=categories.objects.all

        categor=categories.objects.get(id=pk)
        product=products.objects.filter(category=categor)

        return render(request,"index.html",{'products':product,'categories':category})

    else:
        return redirect(login)

def search(request):
    if request.method == 'POST':
        search_item = request.POST['search']
        cache.set('searchitem',search_item)

        item = products.objects.filter(productname__contains=search_item)
        cache.set('item',item)

        return redirect('search')

    else:
        categor=categories.objects.all()
        item=cache.get('item')
        searchitem=cache.get('searchitem')
        print(searchitem)

        cache.delete('searchitem')
        cache.delete('item')

        context = {
            'categor':categor,
            'item':item,
            'searchitem':searchitem
        }

        return render(request,'search.html',context)

# def coupon_check(request):
#     if request.method == 'POST':
#         coupon_code = request.POST['coupon']
#         user=request.user
#         carts=cart.objects.filter(user=user)
#         if Coupon.objects.filter(coupon_code=coupon_code):
#             coupon=Coupon.objects.get(coupon_code=coupon_code)
#             total =request.session['grand_total']
            
        
            
    # else:
    #     return redirect(checkout)        
#def addresses(request):
 #   if request.user.is_authenticated:

  #      retu       pbH1WQD8yIufxQ-vgAYK1vFu87J_FX6ebHilh3Yh