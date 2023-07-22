from django.shortcuts import render,redirect
from app1.models import Category,Product,CartItem,billing_address
from app1.forms import category_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
# for home view
import random
import datetime

# For payment 
import stripe
from app1.payments import PaymentService
from django.conf import settings





# #@login_required
# def home(request):
#     categories = Category.objects.all()  # Retrieve categories from the backend, adjust the query as needed
#     context = {'categories': categories}
#     return render(request, 'index.html', context)


# @login_required
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




@login_required
def update_size(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        cart_item.size = request.POST.get('size')
        cart_item.save()
    return redirect('cart_view')


@login_required
def update_color(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        cart_item.color = request.POST.get('color')
        cart_item.save()
    return redirect('cart_view')




@login_required
def product_detail(request, id):
    one_product = Product.objects.get(id=id)
    categories = Category.objects.all()

 
    return render(request, 'detail.html', {'one_product': one_product, 'categories': categories})

# def product_via_category(request,id):
#     category = Category.objects.get(id=id)
#     categories = Category.objects.all()
#     products = Product.objects.filter(category=category)
    
#     return render(request,'shop.html',{'products':products,'categories':categories})
    
def product_via_category(request, id):
    category = Category.objects.get(id=id)
    categories = Category.objects.all()
    products = Product.objects.filter(category=category)

    paginator = Paginator(products, 12)  # Display 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    search_query = request.GET.get('search')
    if search_query:
     page_obj = products.filter(name__icontains=search_query)
    return render(request, 'shop.html', {'page_obj': page_obj, 'categories': categories,'category':category,'products':products})



# @login_required
# def view_cart(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     total = sum(cartitem.product.price * cartitem.quantity for cartitem in cart_items)
#     categories = Category.objects.all()   
    
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'categories': categories })




################################## CART #######################################################

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
   



##############################  Payment #######################################################

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def process_payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if request.method == 'POST':
        # Retrieve the payment token from the request
        token = request.POST.get('stripeToken')

        try:
            # Create a charge using Stripe
            charge = stripe.Charge.create(
                amount=int(total * 100),  # Stripe requires the amount in cents
                currency='usd',
                description='Payment for products',
                source=token,
            )

            # If the charge is successful, complete the order and do necessary processing
            if charge.status == 'succeeded':
                # Clear the cart items or mark them as purchased

                # Redirect to a success page or display a success message
                return redirect('payment_success')

        except stripe.error.CardError as e:
            # Handle card errors and display an error message to the user
            error = e.user_message

    # Render the payment form with the total amount
    context = {
        'total': total
    }
    return render(request, 'checkout.html', context)





def payment_success(request):
    return render(request, 'success.html')



################################3 SIGN UP #########################################3



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


############################################## BillingAddress  #######################################
@login_required
def add_billing_address(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        country = request.POST.get('country')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Check if the user already has a billing address
        billing_address_object, created = billing_address.objects.get_or_create(user=user)

        billing_address_object.first_name = first_name
        billing_address_object.last_name = last_name
        billing_address_object.email = email
        billing_address_object.mobile_no = mobile_no
        billing_address_object.address_line1 = address_line1
        billing_address_object.address_line2 = address_line2
        billing_address_object.country = country
        billing_address_object.city = city
        billing_address_object.state = state
        billing_address_object.zip_code = zip_code

        billing_address_object.save()
        return redirect('process_payment')

    return render(request, 'BillingAddress.html', {'total': total})


def contact(requset):
    return render(requset,'contact.html',{})



############################################## Email  #######################################
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

@login_required
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send the email
        send_mail(subject, f"Name: {name}\nEmail: {email}\nMessage: {message}", email, [settings.EMAIL_HOST_USER])

        # return HttpResponse('Email sent successfully! ☺☻♥♦♣♠•◘○☺☻☺0♂♀♪♫☼►◄↕‼¶§▬↨↑cd2()*+,-'&%$#"! ▼▲↔∟←→↓↑↨')
        return render(request, 'contact.html', {'success_message': 'Email sent successfully!'})

    return render(request, 'contact.html')

#################################### Admin Views ##################################3



import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from django.db.models import Sum


def update_quantity_sold():
    # Query the quantity sold for each product using aggregation
    quantity_sold_data = CartItem.objects.values('product').annotate(total_quantity_sold=Sum('quantity'))

    # Update the quantity_sold field of each product
    for data in quantity_sold_data:
        product_id = data['product']
        total_quantity_sold = data['total_quantity_sold']
        product = Product.objects.get(pk=product_id)
        product.quantity_sold = total_quantity_sold
        product.save()

def fetch_highest_selling_products_data():
    # Query the products ordered by quantity sold in descending order, along with their categories
    products = Product.objects.select_related('category').order_by('-quantity_sold')

    # Get the highest selling products data along with their categories
    highest_selling_products_data = [
        {
            'product_name': product.name,
            'quantity': product.quantity_sold,
            'category': product.category.category_name  # Assuming category is a ForeignKey to a Category model
        }
        for product in products
    ]

    return highest_selling_products_data

def generate_chart(highest_selling_products_data):
    # Extract product names and quantities
    labels = [item['product_name'] for item in highest_selling_products_data]
    quantities = [item['quantity'] for item in highest_selling_products_data]

    # Generate the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, quantities)
    plt.xlabel('Product')
    plt.ylabel('Quantity Sold')
    plt.title('Highest Selling Products')
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save the bar chart to a file
    chart_filename = 'highest_selling_products_chart.png'
    plt.savefig(chart_filename)

    return chart_filename


def generate_pie_chart(highest_selling_products_data):
    categories = {}
    for item in highest_selling_products_data:
        category_name = item['category']
        quantity_sold = item['quantity']
        if category_name in categories:
            categories[category_name] += quantity_sold
        else:
            categories[category_name] = quantity_sold

    # Extract category names and corresponding quantities
    labels = list(categories.keys())
    quantities = list(categories.values())

    # Generate the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(quantities, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Sales by Category')

    chart_filename = 'category_sales_pie_chart.png'
    plt.savefig(chart_filename)

    return chart_filename




@login_required
def dashboard(request):
    # Update the quantity_sold field before generating the chart and fetching the highest selling products data
    update_quantity_sold()
    categories = Category.objects.all()

    highest_selling_products_data = fetch_highest_selling_products_data()

    # Generate the bar chart and convert it to base64-encoded data
    chart_filename = generate_chart(highest_selling_products_data)

    users = User.objects.all()
    data = []
    for user in users:
        billing_addresss = billing_address.objects.filter(user=user).first()
        cart_items = CartItem.objects.filter(user=user)
        total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
        
        data.append({
            'user': user,
            'billing_address': billing_addresss,
            'cart_items': cart_items,
            'total': total
        })
        for cart_item in cart_items:
            cart_item.total_price_one_product = cart_item.product.price * cart_item.quantity

    # Generate the chart and convert it to base64-encoded data
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.read()).decode('utf-8')

    # Generate the pie chart and convert it to base64-encoded data
    pie_chart_filename = generate_pie_chart(highest_selling_products_data)
    pie_chart_data = encode_image_to_base64(pie_chart_filename)

    context = {
        'data': data,
        'highest_selling_products_data': highest_selling_products_data,
        'chart_data': chart_data,
        'pie_chart_data': pie_chart_data,
        'categories':categories,
    }

    return render(request, 'dashboard/dashboard.html', context)




def encode_image_to_base64(image_filename):
    with open(image_filename, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image



################################### Add and Deletiing ###############################

from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('home')
    template_name = 'confirm_delete.html'  

class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('home')
    template_name = 'confirm_delete.html'  



# def add_color(request):
#     if request.method == 'POST':
#         color = request.POST['color']
#         size = request.POST['size']
#         object_color = color_product.objects.create()
############################################################# ERRoR View

from django.http import Http404

def not_found_view(request):
    return render (request,'404.html')