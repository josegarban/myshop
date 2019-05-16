from .cart import Cart

# With this we'll be able to access the cart in any template
def cart(request):
    return {'cart': Cart(request)}
