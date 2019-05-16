from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST # Decorator to allow only POST requests
def cart_add(request, product_id):
    """
    View for adding products to the cart or updating quantities
    """
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id = product_id)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product         = product,
                 quantity        = cd['quantity'],
                 update_quantity = cd['update'])

    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id = product_id)
    # We retrieve the Product instance with the given ID and remove it
    cart.remove(product)
    # Then, we redirect the user to the cart_detail URL
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
                                                                   # The quantity will be replaced, not added

    return render(request, 'cart/detail.html', {'cart': cart})
