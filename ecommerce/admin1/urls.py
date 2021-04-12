from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin,name="adminlogin"),
    path('adminhome/',views.adminhome,name="adminhome"),
    path('signout/',views.signout,name="signout"),
    path('userdata/',views.userdata,name="userdata"),
    path('userdelete/<int:pk>/',views.userdelete,name="userdelete"),
    path('addcategory/',views.addcategory,name="addcategory"),
    path('categoryview/',views.categoryview,name="categoryview"),
    path('categorydelete/<int:pk>/',views.categorydelete,name="categorydelete"),
    path('blockuser/<int:pk>/',views.blockuser,name="blockuser"),
    path('productadd/',views.productadd,name="productadd"),
    path('productview/',views.productview,name="productview"),
    path('productdelete/<int:pk>/',views.productdelete,name="productdelete"),
    path('productedit/<int:pk>/',views.productedit,name="productedit"),
    path('orderview/',views.orderview,name="orderview"),
    path('order_shipped/<int:pk>/',views.order_shipped,name="order_shipped"),
    path('order_delivered/<int:pk>/',views.order_delivered,name="order_delivered"),
    path('report/',views.report,name="report"),
    path('export_xls_report/',views.export_xls_report,name="export_xls_report"),
    path('export_pdf/',views.export_pdf,name="export_pdf"),
    path('category_discount/<int:pk>/',views.category_discount,name="category_discount"),
    path('view_coupon/',views.view_coupon,name="view_coupon"),
    path('add_coupon/',views.add_coupon,name="add_coupon"),
    path('coupon_delete/<int:pk>/',views.coupon_delete,name="coupon_delete")

    # path('add_offer/',views.add_offer,name="add_offer"),
    # path('view_offers/',views.view_offers,name="view_offers"),
   
    
    
]