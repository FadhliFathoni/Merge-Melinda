from django.urls import path
from . import views

urlpatterns = [
    path('', views.semuaTransaksi),
    path('add/', views.addTransaksi),
    path('filternow/', views.filterSekarang),
    path('filterhari/', views.filterHari),
    path('filterbulan/', views.filterBulan),
    path('filtertahun/', views.filterTahun),
    path('filterrange/', views.filterRange),
]
