from rest_framework import serializers
from .models import Cargos, Orgao

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargos
        fields = '__all__'

class OrgaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orgao
        fields = '__all__'
