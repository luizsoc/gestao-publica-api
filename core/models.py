from django.db import models

class QuadroCargos(models.Model):
    codigo_controle = models.AutoField(primary_key=True)
    nome_quadro = models.CharField(max_length=255)
    
class Cargo(models.Model):
    nome_do_cargo = models.CharField(max_length=255)
    vagas_autorizadas = models.IntegerField(default=0)
    vagas_ocupadas = models.IntegerField(default=0)
    cbo = models.CharField(max_length=10)
    quadro_cargos = models.IntegerField(default=1)  # Apenas armazenando o ID, sem FK

class Orgao(models.Model):
    nome_exibicao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18)
    tipo_orgao = models.CharField(max_length=100)
    municipio = models.CharField(max_length=255)
    codigo_ibge = models.IntegerField(default=0)