from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display=['name','price','created_at','updated_at','is_available','file']
    list_editable=['price','is_available']

class PaymentAdmin(admin.ModelAdmin):
    model  = Payment
    list_display=['user','product','status']

admin.site.register(Product,ProductAdmin)

admin.site.register(Category)

admin.site.register(Payment)

admin.site.register(Userproduct)