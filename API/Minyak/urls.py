from django.urls import path
from . import views

urlpatterns = [
    path('',views.listMinyak),
    path('add/',views.addMinyak),
    path('poin/',views.poinView),
    path('<str:username>',views.detailMinyak),
    path('<str:username>/poin',views.detailPoin),
]
