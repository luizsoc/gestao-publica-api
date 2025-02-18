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
            "Consulta os quadros de cargos com base no nome do quadro "
            "ou no código de controle. Pelo menos um dos parâmetros 'codigo_controle' "
            "ou 'nome_quadro' deve ser informado."
        ),
        manual_parameters=[
            openapi.Parameter("codigo_controle", openapi.IN_QUERY, description="Código de controle.", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter("nome_quadro", openapi.IN_QUERY, description="Nome do quadro.", type=openapi.TYPE_STRING, required=False),
        ],
        responses={
            200: QuadroCargosSerializer(many=True),
            400: "Parâmetros obrigatórios ausentes.",
            404: "Nenhum quadro encontrado para os critérios informados."
        },
    )
    def get(self, request):
        query_params = request.query_params
        codigo_controle = query_params.get("codigo_controle")
        nome_quadro = query_params.get("nome_quadro")

        if codigo_controle:
            quadros = QuadroCargos.objects.filter(codigo_controle=codigo_controle, status=True, revogado=False)
        elif nome_quadro:
            quadros = QuadroCargos.objects.filter(nome_quadro__icontains=nome_quadro, status=True, revogado=False)
        else:
            return Response({"error": "Os parâmetros 'codigo_controle' ou 'nome_quadro' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if not quadros.exists():
            return Response({"error": "Nenhum quadro de cargos encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuadroCargosSerializer(quadros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CargoView(APIView):
    @swagger_auto_schema(
        operation_summary="Consulta de Cargos",
        operation_description="Consulta cargos filtrando por cidade, código IBGE, órgão ou quadro de cargos.",
        manual_parameters=[
            openapi.Parameter("nome_cidade", openapi.IN_QUERY, description="Nome da cidade.", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter("codigo_ibge", openapi.IN_QUERY, description="Código IBGE da cidade.", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter("codigo_orgao", openapi.IN_QUERY, description="Código do órgão.", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter("codigo_controle_quadro_cargos", openapi.IN_QUERY, description="Código do quadro de cargos.", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: CargoSerializer(many=True),
            400: "Parâmetros inválidos ou ausentes.",
            404: "Nenhum cargo encontrado."
        },
    )
    def get(self, request):
        serializer = CargoSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        filtros = {
            "codigo_orgao": serializer.validated_data.get("codigo_orgao"),
            "quadro_cargos_id": serializer.validated_data.get("codigo_controle_quadro_cargos"),
        }
        if serializer.validated_data.get("nome_cidade"):
            filtros["nome_cidade__iexact"] = serializer.validated_data.get("nome_cidade")
        if serializer.validated_data.get("codigo_ibge"):
            filtros["codigo_ibge"] = serializer.validated_data.get("codigo_ibge")

        cargos = Cargo.objects.filter(**filtros)
        if not cargos.exists():
            return Response({"error": "Nenhum cargo encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(CargoSerializer(cargos, many=True).data, status=status.HTTP_200_OK)

class OrgaosView(APIView):
    @swagger_auto_schema(
        operation_summary="Consulta de Órgãos por Município",
        operation_description="Consulta órgãos de um município pelo nome ou código IBGE.",
        manual_parameters=[
            openapi.Parameter("nome_municipio", openapi.IN_QUERY, description="Nome do município.", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter("codigo_ibge", openapi.IN_QUERY, description="Código IBGE do município.", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={
            200: OrgaoSerializer(many=True),
            400: "Informe pelo menos um parâmetro: nome_municipio ou codigo_ibge.",
            404: "Nenhum órgão encontrado."
        },
    )
    def get(self, request):
        nome_municipio = request.query_params.get("nome_municipio")
        codigo_ibge = request.query_params.get("codigo_ibge")

        if not nome_municipio and not codigo_ibge:
            return Response({"error": "Informe pelo menos um dos parâmetros: nome_municipio ou codigo_ibge."}, status=status.HTTP_400_BAD_REQUEST)

        municipio = Municipio.objects.filter(nome__iexact=nome_municipio).first() if nome_municipio else Municipio.objects.filter(codigo_ibge=codigo_ibge).first()
        if not municipio:
            return Response({"error": "Nenhum dado encontrado para o município informado."}, status=status.HTTP_404_NOT_FOUND)

        orgaos = Orgao.objects.filter(municipio=municipio)
        if not orgaos.exists():
            return Response({"error": "Nenhum órgão encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(OrgaoSerializer(orgaos, many=True).data, status=status.HTTP_200_OK)
