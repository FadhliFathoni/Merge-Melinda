from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="API Minyak Documentation",
        default_version='v1',
        description="Documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Account.urls')),    
    path('api_documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api_documentation(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),    
    path("dashboard/",include("API.Dashboard.urls")),
    path('mesin/',include("API.Mesin.urls")),
    path('mesin/',include("API.Mesin.urls")),
    path('minyak/',include("API.Minyak.urls")),
    path('poin/',include("API.Poin.urls")),
    path('produk/',include("API.Produk.urls")),
    path('transaksi/',include("API.Transaction.urls")),
    path('users/',include("API.ManagementUser.urls")),
    path('login/',views.loginView),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)