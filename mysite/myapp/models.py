from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=60)
    image_name = models.CharField(max_length=60)
    api_id = models.IntegerField(primary_key=True,unique = True)

    def __str__(self):
        return f'{self.name}'

class Nutrient(models.Model):
    name = models.CharField(max_length=60)
    amount = models.FloatField(max_length=60)
    unit = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='nutrients')

    def __str__(self):
        return f'{self.name}: {self.amount}{self.unit}'


class ProductListEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_entries')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='entries')