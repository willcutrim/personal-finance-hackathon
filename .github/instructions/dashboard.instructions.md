---
description: "Use quando alterar dashboard: KPIs, agregacoes mensais, contexto da view, graficos Chart.js e responsividade do painel."
applyTo:
  - "dashboard/**"
  - "dashboard/templates/dashboard/**"
  - "static/js/dashboard.js"
  - "static/css/dashboard.css"
---

# Instrucoes do modulo dashboard

## Objetivo
- Manter coerencia entre calculos financeiros, contexto da view e renderizacao visual.
- Evitar regressao de dados e regressao visual no painel.

## Regras de arquitetura
- Regra de agregacao financeira deve ficar em Service, nao na View.
- A View so compoe o contexto para template.
- Se houver consultas dedicadas, usar Repository e nao ORM direto em View.
- Sempre respeitar escopo do usuario autenticado nos dados exibidos.

## Regras de implementacao
- Usar Decimal em calculos monetarios.
- Para percentuais com divisor zero, retornar valor neutro seguro (ex.: None) e tratar na UI.
- Manter contrato de dados estavel entre Service, template e JS.
- Para dados de grafico, tratar estado sem dados para evitar erro de renderizacao.
- Em ajustes de layout, preservar legibilidade dos KPIs em mobile, tablet e desktop.

## Pontos de implementacao
- View e contexto: dashboard/views.py
- Template do painel: dashboard/templates/dashboard/painel.html
- Calculos financeiros: finance/services/saldo_service.py
- Graficos e comportamento cliente: static/js/dashboard.js
- Estilos: static/css/dashboard.css
- Regressao visual: dashboard/visual_regression.py

## Checklist rapido
1. KPI e grafico refletem os mesmos dados de origem.
2. Estado sem dados nao quebra a tela.
3. Layout segue responsivo nos breakpoints principais.
4. Nao ha vazamento de dados entre usuarios.

