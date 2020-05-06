from django.contrib import admin
from .models import Meal, Meal_Type, Size, Item, Meal_Addition, Price

# Register your models here.
admin.site.register(Meal)
admin.site.register(Meal_Type)
admin.site.register(Meal_Addition)
admin.site.register(Size)
admin.site.register(Item)
admin.site.register(Price)