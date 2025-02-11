
# **Minha API Pública**

Bem-vindo à API pública que oferece dados relacionados à gestão de cargos, órgãos e municípios. Este projeto foi desenvolvido com o objetivo de facilitar o acesso às informações e promover transparência na administração pública.

## Índice
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Configuração](#instalação-e-configuração)
- [Endpoints Disponíveis](#endpoints-disponíveis)
- [Modelos Principais](#modelos-principais)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)

## **Tecnologias Utilizadas**
- **Python** (versão 3.9+)
- **Django** (4.0+)
- **Django REST Framework** (DRF)
- **drf-yasg** para documentação Swagger
- Banco de Dados Relacional (como PostgreSQL ou SQLite)

## **Instalação e Configuração**
1. Clone este repositório:
   ```bash
   git clone https://github.com/luizsoc/Projeto-TCMPA
   cd Projeto-TCMPA
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate   # Windows
   ```

3. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```

4. Realize as migrações para configurar o banco de dados:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor local:
   ```bash
   python manage.py runserver
   ```

6. Acesse a aplicação em seu navegador:
   - Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Swagger: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

## **Endpoints Disponíveis**

### 1. **Quadros de Cargos**
- **Rota**: `/api/public/quadros`
- **Método**: GET
- **Descrição**: Filtra e retorna informações sobre quadros de cargos com base nos parâmetros informados.

#### Parâmetros de Consulta (Query Parameters):
| Parâmetro        | Tipo    | Obrigatório | Descrição                           |
|-------------------|---------|--------------|---------------------------------------|
| `nome_cidade`     | String  | Não         | Nome da cidade                        |
| `codigo_ibge`     | Integer | Não         | Código IBGE da cidade                 |
| `orgao_id`        | Integer | Sim          | ID do órgão relacionado ao quadro     |

#### Respostas:
- **200 OK**: Retorna a lista de quadros filtrados.
- **400 Bad Request**: Falha na validação dos parâmetros.
- **404 Not Found**: Nenhum quadro encontrado para os critérios informados.

---

### 2. **Cargos**
- **Rota**: `/api/public/cargos`
- **Método**: GET
- **Descrição**: Retorna informações detalhadas sobre cargos.

#### Parâmetros de Consulta:
| Parâmetro                        | Tipo    | Obrigatório | Descrição                            |
|-----------------------------------|---------|--------------|----------------------------------------|
| `nome_cidade`                     | String  | Não         | Nome da cidade                         |
| `codigo_ibge`                     | Integer | Não         | Código IBGE                            |
| `codigo_orgao`                    | Integer | Sim          | ID do órgão relacionado ao cargo       |
| `codigo_controle_quadro_cargos`   | Integer | Sim          | ID do quadro de cargos relacionado     |

#### Respostas:
- **200 OK**: Retorna a lista de cargos filtrados.
- **400 Bad Request**: Falha na validação dos parâmetros.
- **404 Not Found**: Nenhum cargo encontrado para os critérios informados.

---

### 3. **Órgãos**
- **Rota**: `/api/public/orgaos`
- **Método**: GET
- **Descrição**: Retorna órgãos relacionados a um município.

#### Parâmetros de Consulta:
| Parâmetro       | Tipo    | Obrigatório | Descrição                            |
|------------------|---------|--------------|----------------------------------------|
| `nome_municipio` | String  | Não         | Nome do município                     |
| `codigo_ibge`    | Integer | Não         | Código IBGE                            |

#### Respostas:
- **200 OK**: Retorna a lista de órgãos filtrados.
- **400 Bad Request**: Nenhum parâmetro fornecido.
- **404 Not Found**: Nenhum órgão encontrado para o município informado.

---

## **Modelos Principais**

### QuadroCargos
Armazena informações sobre quadros de cargos.
- **Campos**:
  - `codigo_controle`: ID primário
  - `nome_quadro`: Nome do quadro
  - `data_inclusao` e `data_atualizacao`: Datas automáticas de inclusão e atualização
  - `status`: Status do quadro (ativo, inativo, pendente)
  - `revogado`: Indica se o quadro foi revogado

### Cargo
Armazena informações detalhadas sobre os cargos.
- **Campos**:
  - `nome_do_cargo_vigente`, `vagas_autorizadas`, `vagas_ocupadas`
  - Relacionamentos: Escolaridade, Ordem Profissional, Tipo de Provimento, Ato Legal

### Municipio
Armazena informações sobre municípios.
- **Campos**: `nome`, `codigo_ibge`

### Orgao
Armazena informações sobre órgãos relacionados a municípios.
- **Campos**: `nome_exibicao`, `lei_criacao`, `cnpj`, `tipo_orgao`

## **Como Contribuir**
1. Crie um fork deste repositório.
2. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-branch
   ```
3. Realize os commits das suas alterações:
   ```bash
   git commit -m "Minha contribuição"
   ```
4. Envie as alterações para o seu fork:
   ```bash
   git push origin minha-branch
   ```
5. Abra um Pull Request neste repositório.

## **Licença**
Este projeto está licenciado sob a [MIT License](LICENSE).
