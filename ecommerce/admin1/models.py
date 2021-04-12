from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

class myuser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=12)
    image=models.ImageField(upload_to='media/',null=True)

    @property
    def imgurl4(self):
        if self.image == '':
            image =''
        else:
            image = self.image.url
        return image


class categories(models.Model):
    category = models.CharField(max_length=50)
    discount = models.IntegerField(default=0)

   


class products(models.Model):
    productname = models.CharField(max_length=100)
    category = models.ForeignKey(categories,on_delete = models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=7)
    offer = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to='media/',null=True)
    image2 = models.ImageField(upload_to='media/',null=True)
    image3 = models.ImageField(upload_to='media/',null=True)

    @property
    def discountprice(self):
        discount_value=(self.price/100)*(self.category.discount)
        discount_price=self.price-discount_value
        print(discount_price)
        return discount_price

    @property
    def imageurl(self):
        if self.image1 == '':
            image = ''
        else:
            image = self.image1.url
        return image

    @property
    def imageurl1(self):
        if self.image2 =='':
            image =''
        else:
            image =self.image2.url
        return image        

    @property
    def imageurl2(self):
        if self.image3 == '':
            image =''
        else:
            image =self.image3.url
        return image        

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=10, default='SMALL')
    created_date = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house_name = models.CharField(max_length=50)
    town = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=10, null=True)
    mobile = models.CharField(max_length=20, null=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products=models.ForeignKey(products, on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    price=models.DecimalField(decimal_places=2,max_digits=10)
    payment_method=models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)


class Coupon(models.Model):
    offer = models.IntegerField()
    coupon_code = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)


class Referal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    referal_code = models.CharField(max_length=20)
    offer = models.IntegerField()
    date = models.DateField(auto_now_add=True)


# class Offer(models.Model):
#     category = models.ForeignKey(categories, on_delete=models.CASCADE)
#     name = models.CharField(max_length=32)
#     discount = models.IntegerField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     valid = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name    

        