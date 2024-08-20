from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Payment
from movies.models import Ticket
from django.http import HttpResponse, HttpRequest
from django.contrib import messages

@login_required
def add_to_cart(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, ticket=ticket)
    
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1
    
    cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('ticket')
        total_amount = cart.get_total_amount
        return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})
    except Cart.DoesNotExist:
        return render(request, 'cart/no_cart.html')

@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_amount = cart.get_total_amount
    payment = Payment.objects.create(user=request.user, cart=cart, status='Pending')
    # Simulate payment processing
    messages.info(request, 'Payment processing...')
    payment.status = 'Completed'  # Simulating a successful payment
    payment.save()
    # Clear the cart after payment
    total_amount = cart.get_total_amount
    CartItem.objects.filter(cart=cart).delete()
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'cart/checkout_success.html', {'payment': payment, 'total_amount': total_amount})
