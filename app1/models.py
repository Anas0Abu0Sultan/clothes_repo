from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='products_images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    last_price = models.DecimalField(max_digits=9,decimal_places=2,default=0.00)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #هون انا عندي لينك بين عناصر الكارت وعناصر البرودكت ممكن مجموعة من الكارت ايتم يكومو نفس البرودكت الواحد
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)