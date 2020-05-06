from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy, reverse
from .models import Meal, Item, Meal_Type, Size, Meal_Addition, Price
from .forms import OrderForm
from users.models import Cart
from shopping_cart.models import Order
from django.template.defaulttags import register
from django.contrib.auth.mixins import LoginRequiredMixin
import json


# used to extract values from menu dictionary on the html page
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# Create your views here.

def home(request):
    # get menu data and pass into context
    menu = {}
    price = []
    toppings = []
    sub_additions = {}
    for item in Meal_Type.objects.all():
        l = list(item.meal_addition.values_list('name', flat=True))
        meal_additions_list = [str(i) for i in l]
        sub_additions[item.name] = meal_additions_list
    for item in Meal.objects.all():
        l = list(Meal_Type.objects.filter(meal=item).order_by('name'))
        meal_types_list = [str(i) for i in l]
        menu[item.name] = meal_types_list
    for item in Price.objects.all():
        l = list(item.meal_type.values_list('name', flat=True))
        meal_types_by_price_list = [str(i) for i in l]
        temp = {}
        temp['size'] = item.size
        temp['price'] = item.price
        temp['meal_types'] = meal_types_by_price_list
        price.append(temp)
    meal_additions = Meal_Addition.objects.all()
    for item in list(meal_additions):
        if "Pizza" in str(item):
            toppings.append(item)
    context = {
        'title': 'Home',
        'menu': menu,
        'prices': price,
        'toppings': toppings,
        'sub_additions': sub_additions
    }
    return render(request, 'orders/home.html', context)


# automatically generates the order_form.html page when navigated to
temp = {}
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = OrderForm
    success_url = '/add-to-cart/'
    context_object_name = 'Create'

    def form_valid(self, form):
        # assign the current user as the owner of the order
        form.instance.user = self.request.user
        # assign the price of the order
        form.instance.price = temp['price']
        return super().form_valid(form)


# order form dropdown menu - meal types
def load_meal_type(request):
    meal_id = request.GET.get('meal')
    meal_type = Meal_Type.objects.filter(meal_id=meal_id).order_by('name')
    context = {
        "meal_type": meal_type
    }
    return render(request, 'orders/dropdown_list_options.html', context)


# order form dropdown menu - sizes
def load_size(request):
    temp['meal_type'] = request.GET.get('meal_type')
    size = Size.objects.filter(meal_type=temp['meal_type']).order_by('size')
    context = {
        "size": size
    }
    return render(request, 'orders/dropdown_list_options.html', context)


# order form dropdown menu - meal additions
def load_meal_addition(request):
    # this will only get passed when a different meal type is selected and the additions menu needs to be reset
    if (request.GET.get('meal_type')):
        meal_addition = Meal_Addition.objects.filter(meal_type=(request.GET.get('meal_type'))).order_by('name')
    # this uses the meal type which is saved to temp in the load_size function above
    else:
        meal_addition = Meal_Addition.objects.filter(meal_type=temp['meal_type']).order_by('name')
    context = {
        "meal_addition": meal_addition
    }
    return render(request, 'orders/dropdown_list_options.html', context)


# get the total cost of the meal
# temp1 and temp2 are used in order to calculate the price of any meal additions
temp1 = {}
def load_price(request):
    # if a size is selected then save it and get the price for the meal
    if (request.GET.get('size')):
        temp['size'] = request.GET.get('size')
        meal_price = Price.objects.filter(meal_type=temp['meal_type'], size=temp['size'])
        for item in meal_price:
            temp1['price'] = float(item.price)
            temp['price'] = temp1['price']
        context = {
            "total_price": temp['price']
        }
        return render(request, 'orders/price.html', context)

    # if any meal additions are selected then their price (if any) is added to the total
    if (request.GET.get('meal_addition')):
        meal_additions_list = json.loads(request.GET.get('meal_addition'))
        for each_addition in meal_additions_list:
            temp2 = {'price': 0.0}
            for item in each_addition:
                price = Meal_Addition.objects.get(pk=item)
                if (price.price):
                    temp2['price'] = (temp2['price'] + price.price)
            temp['price'] = (temp1['price'] + temp2['price'])
        context = {
            "total_price": temp['price']
        }
        return render(request, 'orders/price.html', context)


def order_history(request):
    my_user_cart = Cart.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_cart)
    context = {
        'my_orders': my_orders
    }
    return render(request, "orders/history.html", context)