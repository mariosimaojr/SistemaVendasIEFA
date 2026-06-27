# Sistema de Controle de Vendas

Sistema web local para controle de vendas, produtos, estoque, usuários e relatórios, desenvolvido em Python com Django.

O projeto está organizado como uma aplicação Django dentro da pasta `backend`, com módulos separados em apps, templates HTML centralizados e scripts SQL auxiliares para o banco de dados.

## Tecnologias utilizadas

- Python
- Django 6.0.3
- MySQL
- HTML e CSS em templates Django
- JavaScript pontual em templates
- Git e GitHub
- Ambiente virtual Python (`venv`)

As dependências Python do projeto estão listadas em `requirements.txt`:

- `Django`
- `mysqlclient`
- `python-barcode`
- `pillow`
- `python-dotenv`
- dependências de suporte como `asgiref`, `sqlparse` e `tzdata`

## Estrutura do projeto

```text
SistemaVendasIEFA/
├── AGENTS.md
├── README.md
├── requirements.txt
├── BD/
│   ├── 00 - Cria BD controle_vendas_iefa.sql
│   ├── 01 - Ajustes BD controle_vendas_iefa.sql
│   └── 02 - Correções BD controle_vendas_iefa.sql
└── backend/
    ├── manage.py
    ├── venv/
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── apps/
    │   ├── categorias/
    │   ├── formaspagamento/
    │   ├── movimentacoes_estoque/
    │   ├── produtos/
    │   ├── relatorios/
    │   ├── usuarios/
    │   └── vendas/
    ├── templates/
    │   ├── base.html
    │   ├── home.html
    │   ├── categorias/
    │   ├── formaspagamento/
    │   ├── movimentacoes_estoque/
    │   ├── produtos/
    │   ├── relatorios/
    │   ├── usuarios/
    │   └── vendas/
    └── static/
```

## Configuração do ambiente

O ambiente de desenvolvimento confirmado é Windows, com execução local.

Existe Python global na máquina, mas os comandos do projeto devem usar o interpretador do ambiente virtual localizado em:

```powershell
E:\UNIVESP\SistemaVendasIEFA\backend\venv
```

Para trabalhar no backend:

```powershell
cd E:\UNIVESP\SistemaVendasIEFA\backend
```

Ativação opcional do ambiente virtual:

```powershell
.\venv\Scripts\activate
```

Mesmo com o ambiente ativado, prefira comandos explícitos com o Python do `venv` quando for validar ou executar o projeto.

## Instalação de dependências

A partir da pasta `backend`, instale ou atualize as dependências usando o `venv` do projeto:

```powershell
.\venv\Scripts\python.exe -m pip install -r ..\requirements.txt
```

Para validar dependências importantes pelo ambiente correto:

```powershell
.\venv\Scripts\python.exe -c "import django; print(django.get_version())"
.\venv\Scripts\python.exe -c "import MySQLdb, barcode, PIL, dotenv; print('ok')"
```

Não conclua que uma dependência está ausente usando o Python global; valide primeiro com `.\venv\Scripts\python.exe`.

## Execução local

Execute os comandos Django dentro da pasta `backend`:

```powershell
cd E:\UNIVESP\SistemaVendasIEFA\backend
```

Validar configuração do projeto:

```powershell
.\venv\Scripts\python.exe .\manage.py check
```

Iniciar o servidor local:

```powershell
.\venv\Scripts\python.exe .\manage.py runserver
```

Por padrão, o sistema fica disponível em:

```text
http://127.0.0.1:8000/
```

## Banco de dados

O projeto está configurado para usar MySQL local. A configuração atual em `backend\config\settings.py` aponta para o banco `controle_vendas_iefa` em `localhost:3306`.

Os scripts SQL auxiliares ficam em `BD/` e devem ser considerados ao preparar ou ajustar o banco local.

Os modelos atuais usam tabelas existentes do banco, com:

- `db_table`
- `db_column`
- `managed = False`

Além disso, `settings.py` contém `MIGRATION_MODULES` desabilitando migrações para apps existentes. Portanto, mudanças estruturais de banco não devem ser tratadas como migrações Django automáticas sem análise prévia.

## Organização da aplicação

Os módulos da aplicação ficam em `backend\apps` e são referenciados com imports no formato `apps.<nome_do_app>`.

Cada app segue, em geral, a organização Django tradicional:

- `models.py` para modelos ligados às tabelas do banco;
- `forms.py` com `forms.ModelForm` ou `forms.Form`, conforme o fluxo;
- `views.py` com views baseadas em função;
- `urls.py` com `app_name` e rotas do app;
- `templates/<app>/` com telas de listagem, formulário ou relatórios.

As rotas principais são incluídas em `backend\config\urls.py` com `include(...)`.

Os templates usam `backend\templates\base.html` como layout principal, com menu lateral e estilos CSS internos. Alguns fluxos possuem JavaScript diretamente no template, como a tela de vendas.

## Principais módulos e funcionalidades

Os módulos atuais identificados nos fontes são:

- Categorias: listagem, criação, edição e exclusão.
- Formas de pagamento: listagem, criação, edição e exclusão.
- Usuários: listagem, criação, edição e exclusão, com campos de senha no formulário.
- Produtos: listagem, criação, edição e exclusão.
- Movimentações de estoque: listagem, criação, edição e exclusão de entradas e saídas.
- Vendas: listagem, criação, edição e exclusão, com itens de venda via formset e busca de produto por rota JSON.
- Relatórios: página de relatórios, relatório de vendas por forma de pagamento e geração de etiquetas/códigos de barras para produtos.

A página inicial usa um painel simples com atalhos para vendas, produtos e estoque.

## Padrões identificados

- Chaves primárias dos modelos atuais usam o campo `sequencia`.
- Vários modelos mapeiam colunas existentes com nomes em maiúsculas no banco via `db_column`.
- Views usam principalmente `render`, `redirect` e `get_object_or_404`.
- Formulários usam widgets com classes CSS como `form-control`.
- Listagens e formulários seguem templates separados por módulo.
- Relatórios usam formulários próprios e consultas agregadas quando necessário.
- O app de vendas usa `inlineformset_factory` para itens de venda e JavaScript para cálculo de subtotal/total e busca de produto.

Antes de alterar campos, rotas ou templates, confira os fontes reais. Não assuma nomes padrão como `id` sem verificar os modelos, forms e formsets.

## Observações importantes

- Este README descreve o estado atual do repositório e deve ser atualizado conforme o sistema evoluir.
- O projeto roda localmente em Windows e depende de banco MySQL configurado na máquina.
- Use sempre o `venv` do projeto para comandos Python/Django.
- O repositório usa Git/GitHub; trabalhe preferencialmente em branch dedicada.
- Como os modelos atuais não são gerenciados pelo Django, alterações de banco devem ser planejadas junto aos scripts SQL e ao mapeamento dos modelos.
- Existem arquivos `tests.py` nos apps, mas a validação atualmente mais direta é `manage.py check` e teste manual dos fluxos no navegador.

## Manutenção futura

Possíveis melhorias devem ser feitas de forma incremental e alinhada aos padrões já existentes. Pontos úteis para evolução incluem ampliar testes, revisar consistência entre forms/views/templates, documentar mudanças de banco e manter este README sincronizado com a estrutura real do projeto.
