from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('productos', views.ProductListView.as_view(), name='product-list'),
    path('productos/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'), #Lo que va dentro de <> es el tipo de dato. En este caso va el id del producto que es un int y luego el id
    path('registro/', views.RegistrationView.as_view(), name='register'),
]
