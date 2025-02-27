from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cargos, Orgao
from .serializers import CargoSerializer, OrgaoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

logger = logging.getLogger(__name__)

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
        responses={
            200: OrgaoSerializer(many=True),
            400: openapi.Response('Erro: Informe "municipio" ou "codigo_ibge"'),
            404: openapi.Response('Não encontrado')
        },
    )
    def get(self, request):
        municipio = None
        codigo_ibge = None

        # Checar se o corpo da requisição está presente e contém dados
        if request.content_type == 'application/json' and request.body:
            data = request.data  # Acessando o JSON no corpo da requisição
            municipio = data.get("municipio")
            codigo_ibge = data.get("codigo_ibge")
        
        # Se os parâmetros não foram enviados no corpo
        if not municipio and not codigo_ibge:
            return Response({"error": "Informe 'municipio' ou 'codigo_ibge'"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar se os dois parâmetros foram passados, o que não é permitido
        if municipio and codigo_ibge:
            return Response({"error": "Informe apenas um parâmetro: 'municipio' ou 'codigo_ibge'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if municipio:
                logger.info(f"Buscando órgãos com município: {municipio}")
                orgaos = Orgao.objects.filter(municipio__iexact=municipio)
            elif codigo_ibge:
                logger.info(f"Buscando órgãos com código IBGE: {codigo_ibge}")
                orgaos = Orgao.objects.filter(codigo_ibge=codigo_ibge)
            else:
                return Response({"error": "Informe 'municipio' ou 'codigo_ibge'"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erro ao acessar dados: {str(e)}")
            return Response({"error": f"Erro ao acessar os dados: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if not orgaos.exists():
            return Response({"error": "Órgãos não encontrados"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(OrgaoSerializer(orgaos, many=True).data, status=status.HTTP_200_OK)
