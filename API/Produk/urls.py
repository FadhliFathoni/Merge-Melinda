from django.urls import path
from . import views

urlpatterns = [
    path('0', views.produkMany),
    path('0/<str:identifier>', views.produkOne),
    path('tukar', views.tukarPoin),
    path('kategori', views.kategoriMany),
    path('kategori/<str:identifier>', views.kategoriOne)
]
