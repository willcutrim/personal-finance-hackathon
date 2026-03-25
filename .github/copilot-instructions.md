# Instrucoes Gerais do Projeto

Este documento define as regras globais para implementacoes no projeto.
Foco principal: modulo `core` (bases/mixins) e templates base em `templates/`.

## Fluxo oficial de execucao

Toda feature deve seguir este fluxo:

1. Requisicao entra na `View`.
2. Tratamentos da entrada na propria view e/ou `Form` (validacao, filtros, parse de params).
3. Execucao da regra de negocio na camada `Service`.
4. Persistencia e consultas na camada `Repository`.
5. Acesso ao ORM dentro do `Repository` como resultado final da operacao.

Regra obrigatoria:
- Nao pular camadas.
- Nao colocar regra de negocio no template.
- Nao executar ORM diretamente na View quando houver Service para o caso.
- Nao executar ORM diretamente no Service quando houver Repository para o caso.

## Arquitetura do core

### BaseModel e SoftDeleteQueryset

As entidades de dominio usam `BaseModel` (de `core/bases/models.py`) com:
- `criado_em`
- `atualizado_em`
- `deletado_em`

Padrao de exclusao:
- `delete()` faz soft delete.
- `restore()` reativa registro soft deleted.
- `hard_delete()` remove fisicamente.

Managers esperados:
- `objects`: registros ativos.
- `all_objects`: ativos + deletados.

Quando alterar modelos que herdam de `BaseModel`, preservar esse contrato.

### BaseService como centro da regra de negocio

`BaseService` (em `core/bases/services.py`) e a camada padrao de orquestracao de dominio.

Obrigatorio em implementacoes novas:
- Views devem chamar `get_service()`/service da feature para CRUD e listagens.
- `request` e `user` devem ser encapsulados no service (instancia por requisicao).
- Regras de ownership por usuario devem ocorrer no Service (e validacoes complementares no Form quando aplicavel).

### Repository como camada de acesso a dados

Os `Repositorys` (ex.: em `account/repositories/` e `finance/repositories/`) sao a camada oficial para consultas e persistencia.

Obrigatorio em implementacoes novas:
- O Service deve delegar operacoes de dados ao Repository da feature.
- Querysets, filtros ORM, `select_related`/`prefetch_related` e operacoes de escrita devem ficar no Repository.
- A View nao deve acessar Repository diretamente quando houver Service para o caso.

### Bases de view e mixins

Priorizar reutilizacao das bases de `core/bases/views.py` e mixins de `core/mixins.py`:

- `BaseTemplateView`: paginas autenticadas sem CRUD direto.
- `BaseServiceListView`: listagens com service, paginacao e suporte HTMX.
- `BaseServiceCreateView`/`BaseServiceUpdateView`: formularios com `user` injetado em `get_form_kwargs()`.
- `BaseServiceDeleteView`: exclusao com tratamento padrao de `ValidationError` e flash message.

Mixins obrigatorios por contexto:
- `AppLoginRequiredMixin` para paginas autenticadas.
- `AnonymousOnlyMixin` para login/cadastro.
- `FlashMessageMixin` para feedback de sucesso/erro.
- `HtmxRequestMixin` para comportamento dual (request normal vs HTMX).
- `ServiceMixin`/`ServiceObjectMixin` para acesso e lookup seguro do dominio por usuario.

## Convencoes de implementacao por camada

### Views
- Devem coordenar fluxo HTTP, contexto de template e redirecionamentos.
- Podem tratar filtros e parametros de querystring.
- Nao devem concentrar regra de negocio complexa.

### Forms (opcional por caso)
- Usar para validacao de entrada, normalizacao e mensagens de erro de campo.
- Validacoes de seguranca e ownership podem aparecer no Form, mas regra de negocio final permanece no Service.

### Services
- Camada oficial para regra de negocio, CRUD, listagens e operacoes dependentes de usuario.
- Sempre operar no escopo do usuario autenticado da requisicao.
- Devem orquestrar chamadas aos Repositorys sem concentrar detalhes de ORM.

### Repositorys
- Camada oficial para acesso a dados e encapsulamento de ORM.
- Devem expor metodos claros para uso do Service (ex.: listar, obter, criar, atualizar, excluir).
- Devem respeitar o escopo de usuario definido pela regra de negocio da feature.

## Templates base do projeto

Foco apenas em templates estruturais de `templates/`:
- `base.html`
- `base_public.html`
- `base_formulario.html`
- `base_formulario_publico.html`
- `base_list.html`

Diretrizes:
- Reutilizar blocos existentes (`title`, `page_title`, `page_subtitle`, `content`, `extra_css`, `extra_js`).
- Manter includes padrao (`includes/alerts.html`, `includes/page_header.html`, `includes/sidebar.html`, `includes/topbar.html`).
- Em formularios base, preservar contrato do `#base-form`, modal de confirmacao e estados de erro/carregamento.
- Em listagens base, preservar uso de `list_partial_template` e compatibilidade com HTMX.
- Evitar duplicar markup comum em templates de dominio; estender os templates base sempre que possivel.

## HTMX e comportamento de resposta

Quando a view for HTMX-aware:
- Para sucesso com navegacao, retornar `HX-Redirect` (status 204) no fluxo HTMX.
- Para request normal, manter redirect HTTP padrao.
- Em listagens, manter render parcial para HTMX e template completo para request comum.

## Checklist de qualidade obrigatorio

Antes de concluir qualquer alteracao:

1. A implementacao respeita o fluxo `View -> Form/Filters -> Service -> Repositorys -> ORM`.
2. A regra de negocio principal esta no Service.
3. O acesso a dados foi centralizado em Repositorys (sem ORM direto em View/Service, salvo excecao justificada).
4. O escopo por usuario autenticado foi preservado.
5. Soft delete/restore nao foi quebrado para modelos com `BaseModel`.
6. Templates de dominio continuam alinhados aos templates base (sem duplicacao desnecessaria).
7. Fluxos HTMX e nao-HTMX seguem funcionando com resposta correta.

## Resumo de prioridade para o agente

Em caso de duvida de implementacao, seguir esta ordem:

1. Preservar arquitetura em camadas do `core`.
2. Preservar regras de usuario e seguranca de acesso.
3. Reutilizar bases e mixins antes de criar logica nova.
4. Manter consistencia com templates base e includes globais.
