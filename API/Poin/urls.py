from django.urls import path
from . import views

urlpatterns = [
    path('',views.getPoin),
    path('list/',views.ListPoin.as_view())
]
