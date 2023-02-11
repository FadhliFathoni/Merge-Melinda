from django.urls import path
from . import views

urlpatterns = [
    path('',views.ListMinyak.as_view()),
    path('setor/',views.Setoran.as_view()),
    path('setor/<int:id>/verifikasi/',views.Verifikasi),
    path('add/',views.addMinyak),
    path('poin/',views.ListPoin.as_view()),
]
