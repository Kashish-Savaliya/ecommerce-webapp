from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='ShopHome'),
    path('about/', views.about, name='AboutUs'),
    path('contact/', views.contact, name='ContactUs'),
    path('tracker/', views.tracker, name='productTracker'),
    path('products/<int:myId>', views.productView, name='productView'),
    path('search/', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]
