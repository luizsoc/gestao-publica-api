from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse
from django.views.generic import RedirectView #Criamos essa importação para fazer o redirecionamento para o swagger automaticamente
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import QuadroCargosView, CargoView, OrgaosView

schema_view = get_schema_view(
    openapi.Info(
        title="Minha API Pública",
        default_version='v1',
        description="Documentação da API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="email@dominio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'), #Usamos o Redirect para fazer o redirecionamento
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/public/quadros', QuadroCargosView.as_view(), name='quadros-cargos'),
    path('api/public/cargos', CargoView.as_view(), name='cargos'),
    path('api/public/orgaos', OrgaosView.as_view(), name='orgaos'),
]