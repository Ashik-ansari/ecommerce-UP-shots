from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logout,name="logout"),
    path('productdetails/<int:pk>/',views.productdetails,name="productdetails"),
    path('userprofile/',views.userprofile,name="userprofile"),
    path('addtocart/<int:pk>/',views.addtocart,name="addtocart"),
    path('cartview/',views.cartview, name='cartview'),
    path('removecart/<int:pk>/',views.removecart,name="removecart"),
    path('add_quantity/<int:cart_id>', views.add_quantity, name='add_quantity'),
    path('reduce_quantity/<int:cart_id>', views.reduce_quantity, name='reduce_quantity'),
    path('checkout/',views.checkout,name="checkout"),
    path('addaddress/',views.addaddress,name="addaddress"),
    path('addressdelete/<int:pk>/',views.addressdelete,name="addressdelete"),
    path('selectaddress/<int:add_id>',views.selectaddress,name="selectaddress"),
    path('orderpayment/',views.orderpayment,name="orderpayment"),
    path('cod/',views.cod,name="cod"),
    path('paypal/',views.paypal,name="paypal"),
    path('paypalsuccess/',views.paypalsuccess,name="paypalsuccess"),
    path('razorpay/',views.razorpay,name="razorpay"),
    path('razorpaysuccess/',views.razorpaysuccess,name="razorpaysuccess"),
    path('userorders/',views.userorders,name="userorders"),
    path('editprofile/<int:pk>/',views.editprofile,name="editprofile"),
    path('editpassword/',views.editpassword,name="editpassword"),
    path('otp_request/',views.otp_request,name="otp_request"),
    path('otp_validate/',views.otp_validate,name="otp_validate"),
    path('orderstatus/',views.orderstatus,name="orderstatus"),
    path('addimage/',views.addimage,name="addimage"),
    path('order_cancel/<int:pk>/',views.order_cancel,name="order_cancel"),
    path('product_category/<int:pk>/',views.product_category,name="product_category"),
    path('search/',views.search,name="search"),
    path('user_referal/<int:id>/',views.referal_register,name="referal_register"),
    
   # path('referal_register/',views.referal_register,name="referal_register")
    #path('coupon_check/',views.coupon_check,name="coupon_check")
    
]