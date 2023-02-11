from django.urls import path
from . import views
from bson.objectid import ObjectId

urlpatterns = [
    # PRODUK
    path('0', views.ManyProduk.as_view()),
    path('0/<str:pk>', views.OneProduk.as_view()),

    # KATEGORI 
    path('kategori', views.ManyKategori.as_view()),
    path('kategori/<str:pk>', views.OneKategori.as_view()),

    path('tukar', views.tukarPoin)
]
