from django.contrib import admin
from .models import  Product, Nutrient, ProductListEntry
# Register your models here.

admin.site.register(Product)
admin.site.register(Nutrient)
admin.site.register(ProductListEntry)
