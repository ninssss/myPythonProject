from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart


# Create your views here.
def index(request):
    return render(request, "myapp/index.html", {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('myapp:login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Authentication failed
            error_message = "Invalid username or password. Please try again."

    # If request method is not POST or authentication failed, or other cases
    else:
        error_message = None

    return render(request, 'myapp/login.html', {'error_message': error_message})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'myapp/product_detail.html', {'product': product})


def black_opium_detail(request):
    product = Product.objects.get(name='Black Opium')
    return render(request, 'myapp/black_opium.html', {'product': product})


def add_to_cart(request, product_id):
    if 'cart' not in request.session:
        request.session['cart'] = []

    cart = request.session['cart']
    cart.append(product_id)
    request.session['cart'] = cart

    return redirect('myapp:black_opium_detail', product_id=product_id)


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # If user is not authenticated, use session cart data
        cart_item_ids = request.session.get('cart', [])
        cart_items = Product.objects.filter(id__in=cart_item_ids)

    return render(request, 'myapp/cart.html', {'cart_items': cart_items})