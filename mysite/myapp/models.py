from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_vegan = models.BooleanField(default=False)
    is_vegetable = models.BooleanField(default=False)
    is_fruit = models.BooleanField(default=False)
    is_dairy = models.BooleanField(default=False)
    is_legume = models.BooleanField(default=False)  # rosliny straczkowe
    is_meat = models.BooleanField(default=False)
    is_grain = models.BooleanField(default=False)   # zbozowe

    def __str__(self):
        return self.product_name


class Meal(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(Product)
    meal_name = models.CharField(max_length=50)
    meal_difficulty = models.IntegerField(default=0)

    def __str__(self):
        return self.meal_name
