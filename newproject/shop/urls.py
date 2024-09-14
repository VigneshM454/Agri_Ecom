from django.urls import path
from . import views
from .views import showProduct,listProduct,showCart
from django.urls import path


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('', views.home, name='home'),

    path('about/', views.about, name='about'),
    path('contact-us/', views.contact_us, name='contact_us'),

    path('showProduct/<str:prodType>/<int:prodId>',showProduct,name='showProduct'),
    path('listProduct/<str:prodType>',listProduct,name='listProduct'),
    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('removeCart/<int:cart_id>',views.removeCart,name='removeCart'),
    path('buy_product/<int:product_id>',views.buy_product,name='buy_product'),

    path('cart',showCart,name='cart'),

    path('checkout/',views.showCheckout,name='checkout'),


    path('adminPage/',views.adminHome,name='adminHome'),
    path('add-product/', views.add_product, name='add_product'),

]
    # Assuming home view already exists

