from django.urls import path
from . import views
from bson.objectid import ObjectId

urlpatterns = [
    
    # PRODUK
    path('0', views.ManyProduk.as_view()),
    path('0/create', views.createProduk),
    path('0/<str:pk>', views.OneProduk.as_view()),
    path('tukar', views.tukarPoin),

    # KATEGORI 
    path('kategori', views.ManyKategori.as_view()),
    path('kategori/<str:pk>', views.OneKategori.as_view())
]
