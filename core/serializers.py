from rest_framework import serializers
from .models import QuadroCargos, Cargo, Orgao, Municipio

class QuadroCargosSerializer(serializers.ModelSerializer):
    nome_quadro = serializers.CharField(required=False)
    codigo_controle = serializers.CharField(required=False)
    
    class Meta:
        model = QuadroCargos
        fields = "__all__"

    def validate(self, attrs):
        # Garantir que pelo menos um campo esteja preenchido
        if not attrs.get("codigo_controle") and not attrs.get("nome_quadro"):
            raise serializers.ValidationError({
                "detail": "Pelo menos um dos campos 'codigo_controle' ou 'nome_quadro' deve ser informado."
            })
        return attrs
    

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

