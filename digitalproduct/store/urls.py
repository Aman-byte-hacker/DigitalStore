from django.http import request
from django.urls import path
from . import views
from django.conf.urls.static import static
from digitalproduct.settings import MEDIA_URL,MEDIA_ROOT

urlpatterns = [
    path('',views.index,name="index"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('see/<int:product_id>',views.see,name="see"),
    path('orders',views.order,name="order"),
    path('payment/verify',views.paymentverify,name="paymentverify"),
    path('payment/<int:product_id>',views.payment,name="payment")

]+static(MEDIA_URL,document_root=MEDIA_ROOT)