from django.shortcuts import render,redirect
from app1.models import Category,Product,CartItem
from app1.forms import category_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

# for home view
import random
import datetime

# #@login_required
# def home(request):
#     categories = Category.objects.all()  # Retrieve categories from the backend, adjust the query as needed
#     context = {'categories': categories}
#     return render(request, 'index.html', context)


@login_required
def home(request):
    categories = Category.objects.all()
    today = datetime.date.today()
    last_generated_date = request.session.get('random_products_generated_date')
    
    if last_generated_date != today:
        products = list(Product.objects.all())
        random.shuffle(products)
        random_products = products[:8]
        
        # Convert the date object to a string representation
        request.session['random_products_generated_date'] = today.isoformat()
        request.session['random_products'] = [product.pk for product in random_products]
    else:
        random_products_pks = request.session.get('random_products')
        random_products = Product.objects.filter(pk__in=random_products_pks)
    
    context = {
        'categories': categories,
        'random_products': random_products,
    }
    
    return render(request, 'index.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        last_price = request.POST['last_price']
        rating_range = request.POST['rating']
        description = request.POST['description']
        image = request.FILES['image']
        category_id = request.POST['category_id']

        category_object = Category.objects.get(id = category_id)
        product_object = Product.objects.create(
            name = name,
            price = price,
            image = image,
            category = category_object,
            last_price = last_price,
            rating_range=rating_range,
            description=description,
        )
        return redirect('home')
    categories = Category.objects.all()
    return render(request,'add_product.html',{'categories':categories})



@login_required
def add_category(request):
    form = category_form()
    if request.method == "POST":
        form = category_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, 'add_category.html', {'form': form})




def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return render(request, "signup.html", {"error_message": error_message})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        return redirect("login")
    
    return render(request, "signup.html")


# def product_via_category(request,id):
#     category = Category.objects.get(id=id)
#     categories = Category.objects.all()
#     products = Product.objects.filter(category=category)
    
#     return render(request,'shop.html',{'products':products,'categories':categories})
    

def product_via_category(request, id):
    category = Category.objects.get(id=id)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 9)  # Display 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {'page_obj': page_obj, 'categories': categories})





# @login_required
# def view_cart(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     total = sum(cartitem.product.price * cartitem.quantity for cartitem in cart_items)
#     categories = Category.objects.all()   
    
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'categories': categories })

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    categories = Category.objects.all()

    for cart_item in cart_items:
        cart_item.total_price_one_product = cart_item.product.price * cart_item.quantity
        
    total = sum(cartitem.product.price * cartitem.quantity for cartitem in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'categories': categories,'total': total})



@login_required
def cancel_from_cart(request, product_id):
    cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def add_to_cart(request, id):
    product_obj = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(product=product_obj, user=request.user)
    
    if created:
        cart_item.quantity += quantity - 1
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return redirect('cart_view')
   


@login_required
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity_change = request.POST.get('quantity_change')
        if quantity_change == 'increment':
            cart_item.quantity += 1
        elif quantity_change == 'decrement':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart_view')

def product_detail(request,id):
    one_product = Product.objects.get(id=id)
    categories = Category.objects.all()
    return render(request,'detail.html',{'one_product':one_product,'categories':categories})
