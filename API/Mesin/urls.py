from django.urls import path
from . import views

urlpatterns = [
    path('0', views.mesinMany),
    path('0/<str:identifier>', views.mesinOne),
    path('scan', views.scanMesin),
]
