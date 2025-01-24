from django.db import models

class QuadroCargos(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('pendente', 'Pendente'),
    ]

    codigo_controle = models.AutoField(primary_key=True)
    nome_quadro = models.CharField(max_length=255, verbose_name="Nome do Quadro")
    data_inclusao = models.DateField(verbose_name="Data de Inclusão", auto_now_add=True)
    data_atualizacao = models.DateField(verbose_name="Data de Atualização", auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ativo', verbose_name="Status")
    revogado = models.BooleanField(default=False, verbose_name="Revogado")

    def __str__(self):
        return f"{self.nome_quadro} - {self.status}"

    class Meta:
        verbose_name = "Quadro de Cargo"
        verbose_name_plural = "Quadros de Cargos"
        ordering = ['data_inclusao']

class Escolaridade(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class OrdemProfissional(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class AtoLegal(models.Model):
    identificacao = models.CharField(max_length=255)

    def __str__(self):
        return self.identificacao

class TipoProvimento(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Cargo(models.Model):
    nome_do_cargo_vigente = models.CharField(max_length=255)
    data_inicio_vigencia = models.DateField()
    data_fim_vigencia = models.DateField()
    vagas_autorizadas = models.IntegerField()
    vagas_ocupadas = models.IntegerField()
    cargo_acumulavel = models.BooleanField(default=False)
    dedicacao_exclusiva = models.BooleanField(default=False)
    escolaridade_minima = models.ForeignKey(Escolaridade, on_delete=models.CASCADE)
    cbo = models.CharField(max_length=10)
    ordem_profissional = models.ForeignKey(OrdemProfissional, on_delete=models.CASCADE, null=True, blank=True)
    lei_criacao = models.ForeignKey(AtoLegal, on_delete=models.CASCADE)
    tipo_provimento = models.ForeignKey(TipoProvimento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_do_cargo_vigente

class Municipio(models.Model):
    nome = models.CharField(max_length=255)
    codigo_ibge = models.IntegerField(unique=True)

    def __str__(self):
        return self.nome

class Orgao(models.Model):
    nome_exibicao = models.CharField(max_length=255)
    lei_criacao = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18)
    tipo_orgao = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='orgaos')

    def __str__(self):
        return self.nome_exibicao