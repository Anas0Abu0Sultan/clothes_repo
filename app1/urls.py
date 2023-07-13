from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from app1 import views
urlpatterns = [
    path("login/",auth_views.LoginView.as_view(template_name="login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path('signup/',views.signup,name="signup"),
    path("home/",views.home,name="home"),
    path('add_category/', views.add_category, name='add_category'),
    path('add_product/', views.add_product, name='add_product'),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)