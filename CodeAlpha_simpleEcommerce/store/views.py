from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm


def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('/')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('/cart/')
def cart(request):
    cart_ids = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart_ids)

    total = sum(product.price for product in products)

    return render(
        request,
        'cart.html',
        {
            'products': products,
            'total': total
        }
    )

    return render(request, 'cart.html', {'products': products})
def checkout(request):
    cart_ids = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart_ids)

    for product in products:
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            total_price=product.price
        )

    request.session['cart'] = []


    return render(request, 'checkout.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
from django.contrib.auth.decorators import login_required

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(
        request,
        'order_history.html',
        {'orders': orders}
    )