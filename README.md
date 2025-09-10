# API de Câmbio (Django + DRF + PostgreSQL)

Projeto de estudo em **Django Rest Framework**, para cadastro e conversão de moedas.

## Como rodar localmente

### Pré-requisitos
- Python 3.10+
- PostgreSQL instalado e configurado
- Virtualenv ou Conda para gerenciar ambiente

### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/gabrieljdbarros/api_proj.git
   cd api_proj
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` na raiz do projeto:
   ```
   DB_NAME=api_proj_db
   DB_USER=api_user
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## Endpoints principais
- `GET /api/rates/` → lista todas as moedas
- `POST /api/rates/` → adiciona nova moeda
- `PUT /api/rates/{id}/` → atualiza moeda
- `DELETE /api/rates/{id}/` → remove moeda
- `GET /api/rates/convert/` → converte valores entre moedas
