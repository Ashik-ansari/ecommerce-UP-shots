from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from . models import categories,products,Order,Coupon
from django.contrib import messages
from django.core.files import File
import base64
from django.core.files.base import ContentFile
from datetime import date
from django.contrib import messages
from django.http import HttpResponse
import xlwt
import reportlab
from reportlab.pdfgen import canvas
from django.db.models import IntegerField, Model

# Create your views here.

def adminlogin(request):
    if request.session.has_key('key'):
        return redirect ('adminhome')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST['password']
          
        if(username=='ashik' and password =='12345'):
            request.session['key']='high'
            return JsonResponse('true',safe=False)
               
        else:
            return JsonResponse('false',safe=False)
        return redirect(admin1) 
    else:
        return render(request,'adminlogin.html')
    
def adminhome(request):
    if request.session.has_key('key'):

        orders=Order.objects.all()
        orders = orders.count
        total_orders=Order.objects.filter(status='delivered')
        revenue=0
        for i in total_orders:
            revenue = revenue + i.price
            

        users=User.objects.all()
        total_users=users.count

        total_products=products.objects.all()
        product=total_products.count

        today_date=date.today()
        current_month=today_date.month
        order_in_month=Order.objects.filter(date__month=current_month,status="delivered")
        revenue_month=0
        for i in order_in_month:
            revenue_month = revenue_month + i.price
        
       
        order_today=Order.objects.filter(date=today_date,status="delivered")
        revenue_today=0
        for i in order_today:
            revenue_today=revenue_today+i.price
        
        
        return render(request,'adminhome.html',{'total_orders':orders,'total_user':total_users,'total_products':product,'total_revenue':revenue,'revenue_month':revenue_month,'revenues_day':revenue_today})

    else:
        return redirect('adminlogin')

def userdata(request):
        
    if 'search' in request.GET:
        search=request.GET['search']
        users=(User.objects.filter(username__icontains=search) or User.objects.filter(id__icontains=search) or User.objects.filter(first_name__icontains=search) or User.objects.filter(last_name__icontains=search) or  User.objects.filter(email__icontains=search))
        return render(request,'userdata.html',{'users':users})
    else:
        users= User.objects.all()
        return render(request,"userdata.html",{'users':users})
        #else:
          #  return redirect(adminhome)         

def userdelete(request,pk):
    user=User.objects.get(id=pk)
    user.delete()
    return redirect('userdata')


def addcategory(request):
    if request.method == 'POST': 
        print("hoi")
        category = request.POST['category-name']

        if categories.objects.filter(category = category).exists():
            messages.info(request,"This category already exist")
            return redirect('addcategory')

        else:   
            print("category added")
            categories.objects.create(category=category)
            return redirect(addcategory)
        
        
        
            
    else:
        return render(request, 'addcategory.html')

def categoryview(request):
    
    category=categories.objects.all()
    return render(request,"categoryview.html",{'categories':category})

def categorydelete(request,pk):
    category=categories.objects.get(id=pk)
    category.delete()
    return redirect('categoryview')

   

def productadd(request):
    print("haiiiiiii")
    if request.method == 'POST':
        print("hloo")
        category = request.POST['product_category']
        productname = request.POST['product_name']
        price = request.POST['price']
        print(price)
        description = request.POST['description']
        
        
        image1=request.POST['image1']
        format ,imgstr = image1.split(';base64,')
        ext = format.split('/')[-1]
        img1=ContentFile(base64.b64decode(imgstr),name=productname+'.'+ext)

        image2=request.POST['image2']
        format , imgstr2=image2.split(';base64,')
        img2=ContentFile(base64.b64decode(imgstr2),name=productname+'.'+ext)

        image3=request.POST['image3']
        format , imgstr3=image3.split(';base64,')
        img3=ContentFile(base64.b64decode(imgstr3),name=productname+'.'+ext)
       
        category1 = categories.objects.get(category=category)
        product = products.objects.create(category=category1,productname=productname,price=price,image1=img1,image2=img2,image3=img3,description=description)
        product.save()
        print("product created")
        return JsonResponse('true',safe=False)
        
    else:
        category = categories.objects.all()
        return render(request, 'productadd.html', {'categories':category})


def productview(request):
    #if request.session.has_key('key'):
    product=products.objects.all()
    return render(request,"productview.html",{'products':product})


    #if 'search' in request.GET:
     #   search=request.GET['search']
      #  product=(products.objects.filter(productname__icontains=search) or products.objects.filter(id__icontains=search) or products.objects.filter(price__icontains=search) or products.objects.filter(category__icontains=search))
        #return render(request,'productview.html',{'products':product})
    #else:
       

    #else:

     #   return redirect(adminhome)

def productedit(request,pk):
    product = products.objects.get(id=pk)
    category = categories.objects.all()
    context ={'products':product, 'category' : category}
    if request.method == 'POST':
        product_category = request.POST.get('product-category')
        category = categories.objects.get(category=product_category)
        product.category = category
        product.productname = request.POST.get('product-name')
        product.price = request.POST.get('price')
        product.image1 = request.FILES.get('image1')
        product.image2 = request.FILES.get('image2')
        product.image3 = request.FILES.get('image3')
        product.description = request.POST.get('description')
        product.save()
        print("product edited")
        return redirect('productview')

        

    else:
        return render(request, 'productedit.html', context)



def productdelete(request,pk):
    products1=products.objects.get(id=pk)
    products1.delete()
    return redirect('productview')



def blockuser(request,pk):
    user=User.objects.get(id=pk)
    
    if user.is_active == True:
        user.is_active =False
        user.save()
        return redirect('userdata')
    else:
        user.is_active=True
        user.save()
        return redirect('userdata')    

def orderview(request):
    if request.session.has_key('key'):
        order = Order.objects.all
        return render(request,"orderview.html",{'orders':order})
    else:
        return redirect(adminlogin)

def order_shipped(request,pk):
    orders=Order.objects.get(id=pk)
    orders.status = 'shipped'
    orders.save()
    return redirect(orderview)

def order_delivered(request,pk):
    orders=Order.objects.get(id=pk)
    orders.status = 'delivered'
    orders.save()
    return redirect(orderview)

@csrf_exempt
def report(request):
    if request.method == 'POST':
        from_date=request.POST['datefrom']
        to_date=request.POST['todate']
        orders=Order.objects.filter(date__range=[from_date,to_date])
        print(to_date)
        return render(request,"report.html",{'orders':orders})

    else:
        orders=Order.objects.all
        users=User.objects.all
        return render(request,"report.html",{'orders':orders,'user':users})

def export_xls_report(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Order')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['user', 'product' , 'price' , 'quantity', 'status', 'date&time']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()


    rows = Order.objects.all() .values_list('user__username', 'products__productname' , 'price' , 'count', 'status', 'date')
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

    #return render(request,"report.html")

def export_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

    # Create the PDF object, using the response object as its "file."
    row_num=0
    p = canvas.Canvas(response)
    columns = ['user', 'product' , 'price' , 'quantity', 'status', 'date&time']

    for col_num in range(len(columns)):
        p.drawString(row_num, col_num, columns[col_num])

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    rows = p.drawString(100,100,'user__username', 'products__productname' , 'price' , 'count', 'status', 'date')

    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            p.drawString(row_num, col_num, row[col_num])

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


@csrf_exempt
def category_discount(request,pk):
    discount=request.POST['discount']
    print(discount)
    categor=categories.objects.get(id=pk)
    categor.discount=discount
    print(categor)
    categor.save()
    return redirect(categoryview)

    # if request.method == 'POST':
    #     print("houii")
    #     categor=categories.objects.get(id=pk)
    #     category_discount = request.POST['discount']
    #     discounts=categories.objects.create(category=categor,discount=category_discount)
    #     print("created")
    #     return render(request,"categoryview.html",{'discounts':discounts}) 

    # else:
    #     return redirect(categoryview)

# @csrf_exempt
# def add_offer(request):
#     if request.method == 'POST':
#         print("ossss")
#         category_id = request.POST['category']
#         category = categories.objects.get(id=category_id)
#         start_date = request.POST['startDate']
#         end_date = request.POST['endDate']
#         if Offer.objects.filter(category=category, end_date__lte=end_date).exists():
#             print('exists')
#             return JsonResponse('false', safe=False)
#         else:
#             name = request.POST['name']
#             discount = request.POST['discount']

#             Offer.objects.create(category=category, name=name, discount=discount, start_date=start_date, end_date=end_date)
#             return JsonResponse('true', safe=False)
#     else:
#         category = categories.objects.all()
#         context = {
#             'category': category
#         }
#         return render(request, 'add_offer.html', context)


def add_coupon(request):
    if request.method == 'POST':
        discount = request.POST['discount']
        coupon_code = request.POST['coupon_code']

        Coupon.objects.create(offer=discount,coupon_code=coupon_code)
        return redirect(view_coupon)


def view_coupon(request):
    coupon=Coupon.objects.all()
    return render(request,"view_coupon.html",{'Coupon':coupon})

def coupon_delete(request,pk):
    coupon1 = Coupon.objects.get(id=pk)
    coupon1.delete()
    return redirect(view_coupon)



def signout(request):
    request.session.flush()
    return redirect('adminlogin')


