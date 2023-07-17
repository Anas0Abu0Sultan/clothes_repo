from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='categories_images/',null=True)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='products_images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    last_price = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)
    rating_range = models.PositiveIntegerField(default=3)
    description = models.TextField(max_length=4000,default="test Description")

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #هون انا عندي لينك بين عناصر الكارت وعناصر البرودكت ممكن مجموعة من الكارت ايتم يكومو نفس البرودكت الواحد
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price_one_product = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    # total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


class billing_address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
