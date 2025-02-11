from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import QuadroCargos, Cargo, Orgao, Municipio
from .serializers import QuadroCargosSerializer, CargoSerializer, OrgaoSerializer

class QuadroCargosView(APIView):

    @swagger_auto_schema(
        operation_summary="Consulta de Quadros de Cargos",
        operation_description=(
            "Este endpoint permite consultar os quadros de cargos com base no nome do quadro "
            "ou no código de controle. Pelo menos um dos parâmetros 'codigo_controle' ou "
            "'nome_quadro' deve ser informado."
        ),
        manual_parameters=[
            openapi.Parameter(
                "codigo_controle",
                openapi.IN_QUERY,
                description="Código de controle a ser consultado.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "nome_quadro",
                openapi.IN_QUERY,
                description="Nome do quadro a ser consultado.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Consulta realizada com sucesso",
                examples={
                    "application/json": [
                        {
                            "codigo_controle": 101,
                            "nome_quadro": "Quadro Geral de Servidores",
                            "data_inclusao": "2010-01-01",
                            "data_atualizacao": "2023-06-15",
                            "status": "Ativo",
                            "revogado": False,
                        },
                        {
                            "codigo_controle": 102,
                            "nome_quadro": "Quadro de Professores",
                            "data_inclusao": "2015-02-10",
                            "data_atualizacao": "2024-01-01",
                            "status": "Ativo",
                            "revogado": False,
                        },
                    ]
                },
            ),
            400: openapi.Response(
                description="Parâmetros obrigatórios ausentes",
                examples={
                    "application/json": {
                        "error": "Os parâmetros 'codigo_controle ou nome_quadro' são obrigatórios."
                    }
                },
            ),
            404: openapi.Response(
                description="Nenhum quadro de cargos encontrado",
                examples={
                    "application/json": {
                        "error": "Nenhum quadro de cargos encontrado para os critérios informados."
                    }
                },
            ),
        },
    )
    def get(self, request):
        serializer = QuadroCargosSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query_params = request.query_params
        codigo_controle = query_params.get("codigo_controle")
        nome_quadro = query_params.get("nome_quadro")

        # Realizar busca no banco de dados
        if codigo_controle:
            quadros = QuadroCargos.objects.filter(codigo_controle=codigo_controle, status=True, revogado=False)
        elif nome_quadro:
            quadros = QuadroCargos.objects.filter(nome_quadro__icontains=nome_quadro, status=True, revogado=False)
        else: 
            return Response(
                {"error": "Os parâmetros 'codigo_controle' ou 'nome_quadro' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            ) 

        if not quadros.exists():
            return Response(
                {"error": "Nenhum quadro de cargos encontrado para os critérios informados."},
                status=status.HTTP_404_NOT_FOUND,
            )
       
        # Serializar os dados encontrados
        serializer = QuadroCargosSerializer(quadros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CargoView(APIView):

    def get(self, request):
        serializer = CargoSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nome_cidade = serializer.validated_data.get('nome_cidade')
        codigo_ibge = serializer.validated_data.get('codigo_ibge')
        codigo_orgao = serializer.validated_data.get('codigo_orgao')
        codigo_controle_quadro_cargos = serializer.validated_data.get('codigo_controle_quadro_cargos')

        filtros = {'codigo_orgao': codigo_orgao, 'quadro_cargos_id': codigo_controle_quadro_cargos}
        if nome_cidade:
            filtros['nome_cidade__iexact'] = nome_cidade
        if codigo_ibge:
            filtros['codigo_ibge'] = codigo_ibge

        cargos = Cargo.objects.filter(**filtros)
        if not cargos.exists():
            return Response(
                {"error": "Nenhum dado encontrado para os critérios informados."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CargoSerializer(cargos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrgaosView(APIView):

    def get(self, request):
        nome_municipio = request.query_params.get('nome_municipio')
        codigo_ibge = request.query_params.get('codigo_ibge')

        if not nome_municipio and not codigo_ibge:
            return Response(
                {"error": "Informe pelo menos um dos parâmetros: nome_municipio ou codigo_ibge."},
                status=status.HTTP_400_BAD_REQUEST
            )

        municipio = None
        if nome_municipio:
            municipio = Municipio.objects.filter(nome__iexact=nome_municipio).first()
        if not municipio and codigo_ibge:
            municipio = Municipio.objects.filter(codigo_ibge=codigo_ibge).first()

        if not municipio:
            return Response(
                {"error": "Nenhum dado encontrado para o município informado."},
                status=status.HTTP_404_NOT_FOUND
            )

        orgaos = Orgao.objects.filter(municipio=municipio)
        if not orgaos.exists():
            return Response(
                {"error": "Nenhum órgão encontrado para o município informado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrgaoSerializer(orgaos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    