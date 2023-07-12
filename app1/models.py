from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='products_images/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
