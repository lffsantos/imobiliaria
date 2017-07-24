# IMOBILIARIA

## Como desenvolver?

1. clone o respositório.
2. crie um virtualenv com Python 3.5.
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância .env
6. Execute os testes.

```console
git clone git@github.com:lffsantos/imobiliaria.git imobiliaria
cd imobiliaria
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env  
python manage.py makemigrations  
python manage.py migrate  
python manage.py test  
```

## Upload de Imagens para o S3

As imagens do imóvel não são salvas no banco de dados, elas são enviadas para o
s3 e no banco é salvo a url da imagem.
A configuração das credenciais da AWS devem ser configuradas no arquivo '.env'
alterando as variáveis:   
 - AWS_ACCESS_KEY_ID  
 - AWS_SECRET_ACCESS_KEY  
 - AWS_BUCKET  
 
## Criando Super Usuário 

Para cadastrar imóveis é necessario ser um usuário do sistema, rode o comando abaixo para 
criar um super usuário e acesse  o admin para incluir novos.

> python manage.py createsuperuser

## Rodando a aplicação

> python manage.py runserver

## Como Funciona

Para poder cadastrar ou editar um imóvel no sistema é preciso ser um usuário logado

### Gerenciamento 

#### Cadastrar um novo imóvel.

http://localhost:8000/cms/imovel/new

#### Editar imóvel

http://localhost:8000/cms/imovel/edit/<ID\>

#### Lista de Imóveis Cadastrados

http://localhost:8000/admin/core/imovel/

### WebSite

Na url principal o público consegue visualizar os imóveis cadastrados e 
consultar por endereços.

http://localhost:8000/
