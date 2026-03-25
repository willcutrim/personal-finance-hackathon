---
description: "Use quando alterar finance: CRUD de categorias/lancamentos, filtros, HTMX, ownership por usuario e fluxo View -> Form/Filters -> Service -> Repository -> ORM."
applyTo:
  - "finance/**"
  - "finance/templates/finance/**"
---

# Instrucoes do modulo finance

## Objetivo
- Implementar e manter CRUD de categorias e lancamentos com seguranca por usuario.
- Preservar fluxo HTMX e nao-HTMX nas listagens e formularios.

## Arquitetura obrigatoria
1. View coordena request, filtros e resposta (completa ou parcial HTMX).
2. Form/Filters valida entrada.
3. Service centraliza regra de negocio.
4. Repository faz consultas e persistencia.
5. ORM fica somente no Repository.

## Regras do modulo
- Nao colocar regra de negocio no template.
- Nao usar ORM direto em View.
- Nao usar ORM direto no Service quando houver Repository.
- Sempre exigir escopo por usuario autenticado para listar, criar, editar e excluir.
- Em exclusao de categoria, manter bloqueio quando existir lancamento ativo vinculado.
- Em filtros HTMX, preservar estado de querystring e paginacao.

## HTMX
- Em request HTMX de listagem, retornar partial adequada.
- Em sucesso com navegacao no fluxo HTMX, responder com HX-Redirect quando aplicavel.
- Em erro de formulario HTMX, retornar parcial com erros de validacao.
- Em request nao-HTMX, manter redirect/render padrao.

## Pontos de implementacao
- Views e fluxo HTTP: finance/views.py
- Formularios e filtros: finance/forms.py
- Services: finance/services/categoria_service.py, finance/services/lancamento_service.py
- Repositories: finance/repositories/categoria_repository.py, finance/repositories/lancamento_repository.py
- Templates e partials: finance/templates/finance/

## Checklist rapido
1. Fluxo em camadas respeitado sem atalhos.
2. Ownership por usuario validado em todas as operacoes.
3. Filtros por tipo/categoria funcionam com paginacao.
4. HTMX e nao-HTMX funcionam para sucesso e erro.

