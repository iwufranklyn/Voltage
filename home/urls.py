from django.urls import path
from . import views
from . views import Checkout1View


urlpatterns = [
    path('',views.index,name='index'),
    path('contact',views.contact, name='contact'),
    path('products', views.products, name='products'),
    path('details/<str:id>', views.details, name='details'),
    path('signout', views.signout, name='signout'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile_update', views.profile_update, name='profile_update'),
    path('password_update', views.password, name='password'),
    path('shopcart', views.shopcart, name='shopcart'),
    path('displaycart', views.displaycart, name='displaycart'),
    path('deleteitem', views.deleteitem, name='deleteitem'),
    path('increase', views.increase, name='increase'),
    path('checkout1/', Checkout1View.as_view(), name='checkout1'),
    path('pay', views.pay, name= 'pay'),
    path('callback', views.callback, name='callback'),
]
