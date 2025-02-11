import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import QuadroCargos

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def setup_data(db):
    quadro1 = QuadroCargos.objects.create(
        codigo_controle="123",
        nome_quadro="Quadro Teste 1",
        status=True,
        revogado=False,
    )
    quadro2 = QuadroCargos.objects.create(
        codigo_controle="456",
        nome_quadro="Quadro Teste 2",
        status=True,
        revogado=False,
    )
    quadro_revogado = QuadroCargos.objects.create(
        codigo_controle="789",
        nome_quadro="Quadro Revogado",
        status=True,
        revogado=True,
    )
    return [quadro1, quadro2, quadro_revogado]

@pytest.mark.django_db
def test_get_quadro_by_codigo_controle(client, setup_data):
    response = client.get("/api/public/quadros", {"codigo_controle": "123"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["codigo_controle"] == "123"

@pytest.mark.django_db
def test_get_quadro_by_nome_quadro(client, setup_data):
    response = client.get("/api/public/quadros", {"nome_quadro": "Teste"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2  # Deve encontrar quadro1 e quadro2

@pytest.mark.django_db
def test_get_quadro_no_results(client, setup_data):
    response = client.get("/api/public/quadros", {"codigo_controle": "999"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Nenhum quadro de cargos encontrado" in response.data["error"]

@pytest.mark.django_db
def test_get_invalid_params(client):
    response = client.get("/api/public/quadros", {"invalid_param": "value"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
