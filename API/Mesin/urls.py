from django.urls import path
from . import views

urlpatterns = [
    path('0', views.ManyMesin.as_view()),
    path('0/<str:pk>', views.OneMesin.as_view()),
    path('scan', views.scanMesin),
]
