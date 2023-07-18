from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from app1 import views
urlpatterns = [

    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path('signup/',views.signup,name="signup"),

    path("",views.home,name="home"),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),

    path("products/via_categry/<int:id>",views.product_via_category,name="pro_via_cat"),

    path('cart/',views.view_cart,name="cart_view"),
    path('cancel_from_cart/<int:product_id>/', views.cancel_from_cart, name='cancel_from_cart'),
    path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path("add_to_cart/<int:id>",views.add_to_cart,name="add_to_cart"),

    path('product_detail/<int:id>/',views.product_detail,name="product_detail"),

    path('success/', views.payment_success, name='payment_success'),
    path('checkout/', views.process_payment, name='process_payment'),

    path('add/billing/address',views.add_billing_address,name="add_billing_address"),
    path("contact/",views.contact_view,name="contact_view"),

    path('dashboard/', views.dashboard, name='dashboard'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
