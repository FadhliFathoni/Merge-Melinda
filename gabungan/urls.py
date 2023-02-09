from django.contrib import admin
from django.urls import path,include
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Roomrent API Documentation",
        default_version='v1',
        description="Documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('mesin/',include("API.Mesin.urls")),
    path('minyak/',include("API.Minyak.urls")),
    path('produk/',include("API.Produk.urls")),
    path('transaksi/',include("API.Transaction.urls")),
    path('user/',include("API.ManagementUser.urls")),
]
