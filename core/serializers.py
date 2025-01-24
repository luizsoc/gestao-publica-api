from rest_framework import serializers
from .models import QuadroCargos, Cargo, Orgao, Municipio

class QuadroCargosSerializer(serializers.ModelSerializer):
    nome_cidade = serializers.CharField(required=False, allow_blank=True)
    codigo_ibge = serializers.IntegerField(required=False, allow_null=True)
    orgao_id = serializers.IntegerField(required=True)

    class Meta:
        model = QuadroCargos
        fields = [
            'codigo_controle',
            'nome_quadro',
            'data_inclusao',
            'data_atualizacao',
            'status',
            'revogado',
            'nome_cidade',
            'codigo_ibge',
            'orgao_id',
        ]

    def validate(self, attrs):
        nome_cidade = attrs.get('nome_cidade')
        codigo_ibge = attrs.get('codigo_ibge')
        orgao_id = attrs.get('orgao_id')

        if not orgao_id:
            raise serializers.ValidationError({"orgao_id": "O parâmetro 'orgao_id' é obrigatório."})

        if not nome_cidade and not codigo_ibge:
            raise serializers.ValidationError(
                {"non_field_errors": "Os parâmetros 'nome_cidade' ou 'codigo_ibge' devem ser informados."}
            )

        return attrs

    def get_filtered_data(self):
        nome_cidade = self.validated_data.get('nome_cidade')
        codigo_ibge = self.validated_data.get('codigo_ibge')
        orgao_id = self.validated_data.get('orgao_id')

        filtros = {'orgao_id': orgao_id}
        if nome_cidade:
            filtros['nome_cidade__iexact'] = nome_cidade
        if codigo_ibge:
            filtros['codigo_ibge'] = codigo_ibge

        return QuadroCargos.objects.filter(**filtros)

class CargoSerializer(serializers.ModelSerializer):
    nome_cidade = serializers.CharField(required=False, allow_blank=True)
    codigo_ibge = serializers.IntegerField(required=False, allow_null=True)
    codigo_orgao = serializers.IntegerField(required=True)
    codigo_controle_quadro_cargos = serializers.IntegerField(required=True)

    class Meta:
        model = Cargo
        fields = [
            'nome_do_cargo_vigente',
            'data_inicio_vigencia',
            'data_fim_vigencia',
            'vagas_autorizadas',
            'vagas_ocupadas',
            'cargo_acumulavel',
            'dedicacao_exclusiva',
            'escolaridade_minima',
            'cbo',
            'ordem_profissional',
            'lei_criacao',
            'tipo_provimento',
            'nome_cidade',
            'codigo_ibge',
            'codigo_orgao',
            'codigo_controle_quadro_cargos',
        ]

    def validate(self, attrs):
        nome_cidade = attrs.get('nome_cidade')
        codigo_ibge = attrs.get('codigo_ibge')
        codigo_orgao = attrs.get('codigo_orgao')
        codigo_controle_quadro_cargos = attrs.get('codigo_controle_quadro_cargos')

        if not nome_cidade and not codigo_ibge:
            raise serializers.ValidationError(
                {"non_field_errors": "Os parâmetros 'nome_cidade' ou 'codigo_ibge' devem ser informados."}
            )

        if not codigo_orgao:
            raise serializers.ValidationError({"codigo_orgao": "O parâmetro 'codigo_orgao' é obrigatório."})

        if not codigo_controle_quadro_cargos:
            raise serializers.ValidationError({"codigo_controle_quadro_cargos": "O parâmetro 'codigo_controle_quadro_cargos' é obrigatório."})

        return attrs

class OrgaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orgao
        fields = [
            'id',
            'nome_exibicao',
            'lei_criacao',
            'cnpj',
            'tipo_orgao'
        ]

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ['nome', 'codigo_ibge']

