---
name: finance
description: 'WORKFLOW SKILL para o modulo finance (categorias e lancamentos) em Django com camadas Form + View + Service + Repository. Use para criar/ajustar CRUD, filtros por tipo/categoria, validacoes por usuario autenticado e fluxos HTMX com checagens de regressao.'
argument-hint: 'Descreva a tarefa no finance: ex. "novo filtro de lancamentos" ou "regra para excluir categoria"'
user-invocable: true
---

# Finance Module Workflow

## Quando usar
- Implementar ou corrigir CRUD de lancamentos e categorias.
- Ajustar filtros de listagem (tipo e categoria) e comportamento de paginacao.
- Alterar validacoes de formulario e regras de negocio por usuario autenticado.
- Evoluir fluxos HTMX (partial render, HX-Redirect, filtros sem reload completo).
- Revisar seguranca de ownership e integridade de dados financeiros.

## Contexto do projeto
- App `finance` concentra categorias e lancamentos de receitas/despesas.
- Arquitetura em camadas: Forms -> Views (CBVs base) -> Services -> Repositories.
- Listagens usam suporte HTMX com templates parciais.
- Regras de calculo de saldo e agregacao ficam em `SaldoService`.

## Procedimento padrao
1. Classificar a tarefa: formulario, regra de negocio, persistencia, listagem HTMX ou UX da tela.
2. Identificar fluxo ponta a ponta: URL -> View -> Service -> Repository -> Template/Partial.
3. Aplicar a mudanca na camada correta (evitar logica de dominio na View/Template).
4. Validar casos de sucesso e erro (mensagens flash, filtros, ownership, redirecionamentos).
5. Executar regressao minima de listagens, CRUD e comportamento HTMX.

## Mapa rapido de arquivos
- Rotas: `finance/urls.py`
- Views: `finance/views.py`
- Forms: `finance/forms.py`
- Models: `finance/models.py`
- Services: `finance/services/categoria_service.py`, `finance/services/lancamento_service.py`, `finance/services/saldo_service.py`
- Repositories: `finance/repositories/categoria_repository.py`, `finance/repositories/lancamento_repository.py`
- Templates: `finance/templates/finance/`
- Partials HTMX: `finance/templates/finance/partials/`
- Testes: `finance/tests.py`

## Regras de decisao
### Se a mudanca for validacao de entrada
- Preferir `finance/forms.py` para validacoes de campo (ex.: valor > 0, categoria do usuario).
- Usar mensagens de erro claras e orientadas a acao.

### Se a mudanca for regra de negocio
- Implementar em `finance/services/*.py`.
- Garantir ownership por usuario autenticado nas operacoes criticas.
- Em exclusao de categoria, preservar bloqueio quando houver lancamentos ativos vinculados.

### Se a mudanca for persistencia/consulta
- Implementar em `finance/repositories/*.py`.
- Exigir `user` explicitamente nas consultas e mutacoes.
- Manter filtros de tipo/categoria e agregacoes no repositorio, nao na View.

### Se a mudanca for listagem ou filtro
- Ajustar `finance/views.py` em conjunto com partials em `finance/templates/finance/partials/`.
- Preservar contrato HTMX: `HX-Request`, partial render e `HX-Redirect` quando aplicavel.
- Garantir consistencia entre querystring, paginacao e estado dos filtros.

### Se a mudanca for tela/UX
- Ajustar template principal (`finance/templates/finance/*.html`) para estrutura da pagina.
- Ajustar partials para tabela, filtros e estado vazio.
- Preservar feedback visual de receitas/despesas (badges, sinal +/-, moeda).

## Checklist de implementacao
1. Confirmar escopo: categoria, lancamento, filtro, HTMX, saldo ou layout.
2. Atualizar a camada principal da mudanca (Form, Service ou Repository).
3. Ajustar View para repassar contexto/filtros corretamente.
4. Sincronizar templates/partials com dados esperados.
5. Revisar seguranca de acesso por usuario em list/create/update/delete.
6. Revisar mensagens de sucesso/erro e fluxo de redirecionamento.
7. Atualizar ou criar testes no app finance.

## Checklist de qualidade (Definition of Done)
- Nao existe acesso cross-user a categorias ou lancamentos.
- Validacoes essenciais estao cobertas (valor positivo, categoria do usuario, nome unico por usuario).
- Filtros por tipo/categoria funcionam com paginacao sem perder estado.
- Fluxo HTMX responde corretamente com partial e/ou `HX-Redirect`.
- Exclusao de categoria respeita regra de bloqueio por lancamentos ativos.
- KPIs/saldo exibidos nas listagens permanecem consistentes com os dados persistidos.

## Comandos uteis
```bash
python manage.py test finance
python manage.py test finance.tests.FinanceListHtmxTests
python manage.py runserver
```

## Prompts de exemplo
- "/finance adicionar filtro por periodo na listagem de lancamentos com HTMX"
- "/finance bloquear edicao de categoria quando nome duplicar para o mesmo usuario"
- "/finance revisar seguranca de ownership em create/update/delete de lancamentos"
- "/finance ajustar modal de nova movimentacao e manter comportamento de erro no formulario"

