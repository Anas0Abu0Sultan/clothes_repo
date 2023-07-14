from django.shortcuts import render,redirect
from app1.models import Category,Product,CartItem
from app1.forms import category_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# @login_required
def home(request):
    categories = Category.objects.all()  # Retrieve categories from the backend, adjust the query as needed
    context = {'categories': categories}
    return render(request, 'index.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        category_id = request.POST['category_id']

        category_object = Category.objects.get(id = category_id)
        product_object = Product.objects.create(
            name = name,
            price = price,
            image = image,
            category = category_object
        )
        return redirect('home')
    categories = Category.objects.all()
    return render(request,'add_product.html',{'categories':categories})





@login_required
def add_category(request):
    form = category_form()
    if request.method == "POST":
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request,'add_category.html',{'form':form})




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


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(cartitem.product.price * cartitem.quantity for cartitem in cart_items )
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})
