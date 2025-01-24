from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QuadroCargos, Cargo, Orgao, Municipio
from .serializers import QuadroCargosSerializer, CargoSerializer, OrgaoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class QuadroCargosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = QuadroCargosSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        quadros = serializer.get_filtered_data()
        if not quadros.exists():
            return Response(
                {"error": "Nenhum quadro de cargos encontrado para os critérios informados."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuadroCargosSerializer(quadros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CargoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = CargoSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        nome_cidade = serializer.validated_data.get('nome_cidade')
        codigo_ibge = serializer.validated_data.get('codigo_ibge')
        codigo_orgao = serializer.validated_data.get('codigo_orgao')
        codigo_controle_quadro_cargos = serializer.validated_data.get('codigo_controle_quadro_cargos')

        filtros = {'codigo_orgao': codigo_orgao, 'id': codigo_controle_quadro_cargos}
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
    permission_classes = [AllowAny]
    
    def get(self, request):
        nome_municipio = request.query_params.get('nome_municipio')
        codigo_ibge = request.query_params.get('codigo_ibge')

        if not nome_municipio and not codigo_ibge:
            return Response(
                {"error": "Informe pelo menos um dos parâmetros: nome_municipio ou codigo_ibge."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if nome_municipio:
                municipio = Municipio.objects.get(nome__iexact=nome_municipio)
            elif codigo_ibge:
                municipio = Municipio.objects.get(codigo_ibge=codigo_ibge)
        except Municipio.DoesNotExist:
            return Response(
                {"error": "Nenhum dado encontrado para o município informado."},
                status=status.HTTP_404_NOT_FOUND
            )

        orgaos = Orgao.objects.filter(municipio=municipio)
        if not orgaos.exists():
            return Response(
                {"error": "Nenhum dado encontrado para o município informado."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrgaoSerializer(orgaos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

