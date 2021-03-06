from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from users.models import Cart
from orders.models import Item
from shopping_cart.extras import generate_order_id
from shopping_cart.models import OrderItem, Order, Transaction
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def get_user_pending_order(request):
    # get order for the correct user
    user_cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.filter(owner=user_cart, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request):
    # get the user cart
    user_cart = get_object_or_404(Cart, user=request.user)
    # filter items by latest
    item = Item.objects.filter(user=request.user).order_by('timestamp').last()

    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(item=item)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_cart, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.success(request, "Item added to cart!")
    context = {
        'title': 'Cart'
    }
    return redirect('shopping_cart:order_summary')


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted!")
    return redirect(reverse('shopping_cart:order_summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order,
        'title': 'Cart'
    }
    return render(request, 'shopping_cart/order_summary.html', context)


@login_required()
def checkout(request):
    existing_order = get_user_pending_order(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            charge = stripe.Charge.create(amount=int(100*existing_order.get_cart_total()), currency='usd', description='Example charge', source=token)
            return redirect(reverse('shopping_cart:update_records', kwargs={'token': token}))
        except stripe.CardError as e:
            messages.warning(request, "Your card has been declined.")

    context = {
        'order': existing_order,
        'STRIPE_PUBLISHABLE_KEY': publishKey,
        'title': 'Checkout'
    }
    return render(request, 'shopping_cart/checkout.html', context)


@login_required()
def update_transaction_records(request, token):
    # get the order being processed
    order_to_purchase = get_user_pending_order(request)

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # add products to user cart
    user_cart = get_object_or_404(Cart, user=request.user)
    # get the products from the items
    order_products = [item.item for item in order_items]
    user_cart.item.add(*order_products)
    user_cart.save()

    # create a transaction
    transaction = Transaction(cart=request.user.cart, token=token, order_id=order_to_purchase.id, amount=order_to_purchase.get_cart_total(), success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.success(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('orders-history'))


def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})