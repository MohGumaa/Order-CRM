from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = "users"

urlpatterns = [
    path('register/', views.registerPage , name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html",redirect_authenticated_user=True) , name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('user/', views.user_page , name="user-page"),
    path('account/', views.customerSettings , name="account"),
    path('', views.home , name="home"),
    path('product/', views.product , name="product"),
    path('customer/<int:id>/', views.customer, name="customer"),
    path('create_order/<int:id>', views.createOrder, name="create_order"),
    path('update_order/<int:id>', views.updateOrder, name="update_order"),
    path('delete_order/<int:id>', views.deleteOrder, name="delete_order"),
]

