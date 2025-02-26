from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import CargoView, OrgaoView

schema_view = get_schema_view(
   openapi.Info(
      title="API de Gestão Pública",
      default_version='v1',
      description="Documentação da API para consulta de cargos e órgãos públicos",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@exemplo.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/cargos', CargoView.as_view(), name='cargos'),
    path('api/orgaos', OrgaoView.as_view(), name='orgaos'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
