from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cargos, Orgao
from .serializers import CargoSerializer, OrgaoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CargoView(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtém todos os cargos",
        responses={200: CargoSerializer(many=True)},
    )
    def get(self, request):
        cargos = Cargos.objects.all()
        return Response(CargoSerializer(cargos, many=True).data, status=status.HTTP_200_OK)

class OrgaoView(APIView):
    
    @swagger_auto_schema(
        operation_description="Obtém órgãos filtrados por município ou código IBGE",
        manual_parameters=[
            openapi.Parameter('municipio', openapi.IN_QUERY, description="Nome do município", type=openapi.TYPE_STRING),
            openapi.Parameter('codigo_ibge', openapi.IN_QUERY, description="Código IBGE", type=openapi.TYPE_INTEGER),
        ],
        responses={200: OrgaoSerializer(many=True)},
    )
    def get(self, request):
        municipio = request.query_params.get("municipio")
        codigo_ibge = request.query_params.get("codigo_ibge")
        
        if municipio:
            orgaos = Orgao.objects.filter(municipio__iexact=municipio)
        elif codigo_ibge:
            orgaos = Orgao.objects.filter(codigo_ibge=codigo_ibge)
        else:
            return Response({"error": "Informe 'municipio' ou 'codigo_ibge'"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(OrgaoSerializer(orgaos, many=True).data, status=status.HTTP_200_OK)
