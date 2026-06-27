# AGENTS.md

Instruções persistentes para futuras sessões do Codex neste repositório.

## Contexto do projeto

Este repositório contém um sistema local de controle de vendas desenvolvido em Django/Python, com banco MySQL e interface baseada em templates HTML do Django.

A raiz do repositório é:

```powershell
E:\UNIVESP\SistemaVendasIEFA
```

A aplicação Django fica em:

```powershell
E:\UNIVESP\SistemaVendasIEFA\backend
```

A estrutura atual confirma:

- `backend\manage.py`: entrada de comandos Django.
- `backend\config`: configuração principal, rotas globais, ASGI/WSGI e view inicial.
- `backend\apps`: módulos Django da aplicação. A estrutura pode crescer com novos apps no futuro.
- `backend\templates`: templates centralizados, incluindo `base.html` e pastas por área funcional.
- `backend\static`: diretório reservado para arquivos estáticos.
- `BD`: scripts SQL auxiliares do banco de dados.
- `requirements.txt`: dependências Python controladas do projeto.

Não trate a lista atual de apps como definitiva. O sistema está em evolução.

## Ambiente e execução

O ambiente de desenvolvimento é Windows e o projeto roda localmente.

Existe Python global na máquina, mas comandos do projeto devem priorizar o Python do ambiente virtual do próprio projeto:

```powershell
E:\UNIVESP\SistemaVendasIEFA\backend\venv
```

Para comandos Django, execute dentro de `backend` usando explicitamente:

```powershell
.\venv\Scripts\python.exe .\manage.py <comando>
```

Exemplos úteis:

```powershell
cd E:\UNIVESP\SistemaVendasIEFA\backend
.\venv\Scripts\python.exe .\manage.py check
.\venv\Scripts\python.exe .\manage.py runserver
.\venv\Scripts\python.exe -c "import django; print(django.get_version())"
```

Antes de concluir que uma dependência Python está ausente ou que o ambiente está quebrado, valide usando `.\venv\Scripts\python.exe`. As dependências do projeto devem ser conferidas em `requirements.txt`.

## Regras de análise

- Leia os fontes atuais antes de propor qualquer alteração.
- Não assuma nomes de apps, rotas, templates, modelos, campos, chaves primárias ou convenções sem verificar nos arquivos.
- Respeite a estrutura real do projeto e o modo como cada camada está integrada.
- Quando a mudança puder afetar mais de uma camada, analise o fluxo completo: `models.py`, `forms.py`, `views.py`, `urls.py`, templates, scripts e dados relacionados.
- Considere que o projeto pode conter padrões herdados ou parcialmente evoluídos. Não use apenas o `README.md` como fonte única de verdade.
- Evite conclusões baseadas no Python global da máquina.

## Regras de alteração

Trabalhe em modo de planejamento + execução controlada:

1. Analise os arquivos relevantes.
2. Explique a causa do problema ou a justificativa da melhoria.
3. Liste os arquivos que pretende alterar.
4. Aguarde aprovação antes de modificar arquivos, salvo quando o usuário pedir explicitamente a criação ou alteração direta de um arquivo específico.
5. Não altere arquivos fora do escopo pedido.

Ao editar, mantenha consistência entre backend, formulários, views, rotas, templates e banco de dados. Não assuma automaticamente campos padrão como `id`; confira os modelos e os campos reais gerados por forms/formsets.

Evite reestruturações amplas sem necessidade. Prefira correções pequenas, compreensíveis e alinhadas ao padrão local.

## Regras de validação

Ao concluir uma alteração, informe comandos de validação quando fizer sentido. Priorize validações com o Python do `venv`, por exemplo:

```powershell
cd E:\UNIVESP\SistemaVendasIEFA\backend
.\venv\Scripts\python.exe .\manage.py check
```

Para fluxos funcionais, considere validação manual no navegador local, especialmente quando houver mudanças em templates, formulários, JavaScript ou rotas.

Sempre sugira uma validação manual objetiva ao final quando a mudança envolver comportamento de tela, cadastro, edição, exclusão, relatórios ou integração com banco.

## Git e Codex

O projeto usa Git e GitHub. No Codex, trabalhe preferencialmente em branch dedicada e evite alterações diretas na branch principal.

Antes e depois de mudanças, confira o estado do repositório quando isso ajudar a separar alterações do usuário das alterações da sessão:

```powershell
git status
git branch --show-current
```

Ao final de uma alteração, informe:

- arquivos alterados;
- resumo claro do que mudou;
- validações executadas ou pendentes.

Não reverta alterações existentes sem pedido explícito do usuário.

## Convenções e pontos de atenção identificados

- Os apps Django ficam sob `backend\apps` e usam imports no formato `apps.<nome_do_app>`.
- As rotas globais em `config\urls.py` incluem rotas de apps com `include(...)`.
- Os templates estão centralizados em `backend\templates`, com `BASE_DIR / 'templates'` configurado em `settings.py`.
- Os modelos atuais usam tabelas existentes do banco, com `db_table`, `db_column` e `managed = False`.
- `settings.py` contém configuração MySQL local e desabilita migrações para apps já existentes por meio de `MIGRATION_MODULES`.
- Forms são, em geral, baseados em `forms.ModelForm`.
- Views atuais usam majoritariamente funções com `render`, `redirect` e `get_object_or_404`.
- Há scripts SQL em `BD`; mudanças de banco devem considerar esses artefatos e a configuração dos modelos não gerenciados pelo Django.
- O layout base e estilos principais estão em `templates\base.html`.
- Alguns fluxos usam integração entre template e JavaScript; nesses casos, valide nomes de campos, URLs e dados esperados pela view.
- Foram observadas inconsistências pontuais entre formsets/templates em fluxos existentes. Antes de corrigir ou expandir telas com formsets, confira os campos ocultos reais gerados pelo Django e não presuma nomes padrão.

Este arquivo deve orientar o trabalho futuro sem congelar a arquitetura. Novos módulos podem ser adicionados, desde que respeitem os padrões comprovados ou documentem claramente novas decisões.
