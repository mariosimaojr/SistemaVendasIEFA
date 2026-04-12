# Sistema de Controle de Vendas

## Descrição

Este projeto tem como objetivo o desenvolvimento de um **Sistema de
Controle de Vendas**, implementado utilizando o framework **Django** em
Python.\
O sistema foi concebido como parte de um projeto acadêmico, com foco em
boas práticas de desenvolvimento, organização de código e padronização
de estrutura.

A aplicação permite o gerenciamento de informações relacionadas a
categorias, produtos, vendas e movimentações de estoque, servindo como
base para evolução incremental de funcionalidades.

------------------------------------------------------------------------

## Objetivos do Projeto

-   Implementar um sistema web para controle básico de vendas
-   Aplicar boas práticas de modelagem de banco de dados
-   Utilizar arquitetura organizada em módulos (apps)
-   Padronizar nomenclaturas e estrutura do projeto
-   Servir como referência didática para desenvolvimento em equipe

------------------------------------------------------------------------

## Tecnologias Utilizadas

-   Python 3.x
-   Django
-   MySQL
-   HTML
-   CSS
-   Git / GitHub
-   Ambiente virtual (venv)

------------------------------------------------------------------------

## Estrutura do Projeto

    backend/
    │
    ├── apps/
    │   └── categorias/
    │       ├── models.py
    │       ├── views.py
    │       ├── forms.py
    │       ├── urls.py
    │       └── migrations/
    │
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── templates/
    │   ├── base.html
    │   └── categorias/
    │       ├── lista.html
    │       └── form.html
    │
    ├── static/
    ├── manage.py
    └── requirements.txt

------------------------------------------------------------------------

## Padrões e Convenções

-   Tabelas no plural
-   Colunas no singular
-   Nomes em snake_case
-   Organização modular utilizando apps
-   Separação clara entre camadas (models, views, templates)

------------------------------------------------------------------------

## Como executar o projeto

### 1) Clonar o repositório

    git clone <url-do-repositorio>
    cd projeto

### 2) Ativar ambiente virtual

Windows:

    venv\Scripts\activate

Linux / Mac:

    source venv/bin/activate

### 4) Instalar dependências

    pip install -r requirements.txt

### 5) Iniciar servidor

    python manage.py runserver

A aplicação estará disponível em:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

## Funcionalidades Implementadas

-   Cadastro de Categorias
-   Listagem de Categorias
-   Estrutura base do sistema
-   Integração com banco de dados
-   Templates e layout inicial

------------------------------------------------------------------------

## Próximas Evoluções

-   Cadastro de Produtos
-   Controle de Estoque
-   Registro de Vendas
-   Relatórios
-   Autenticação de usuários
-   Interface com Bootstrap

------------------------------------------------------------------------

## Boas Práticas Adotadas

-   Versionamento com Git
-   Commits descritivos
-   Padronização de nomenclaturas
-   Estrutura organizada por módulos
-   Separação de responsabilidades

------------------------------------------------------------------------

## Autor

Projeto acadêmico desenvolvido como base para estudo e evolução de
práticas de desenvolvimento de sistemas web.
