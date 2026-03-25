---
name: dashboard
description: 'WORKFLOW SKILL para o modulo dashboard (painel, KPIs, calculos mensais e graficos) em Django. Use para criar/ajustar regras de agregacao financeira, contexto da view, layout responsivo e renderizacao Chart.js com checagens de regressao visual.'
argument-hint: 'Descreva a tarefa no dashboard: ex. "novo KPI no painel" ou "ajustar grafico de despesas"'
user-invocable: true
---

# Dashboard Module Workflow

## Quando usar
- Implementar ou corrigir calculos de KPIs no painel financeiro.
- Ajustar montagem de contexto da view do dashboard.
- Alterar datasets e comportamento dos graficos (linha, donut e barras).
- Refinar layout e responsividade do painel.
- Investigar regressao visual ou inconsistencia entre dados e UI.

## Contexto do projeto
- Dashboard principal: view `PainelView` com template `dashboard/painel.html`.
- Dados financeiros consolidados em `SaldoService`.
- Graficos renderizados no frontend com Chart.js via `static/js/dashboard.js`.
- Estilo do painel e componentes KPI em `static/css/dashboard.css`.
- Suite de regressao visual por breakpoint em `dashboard/visual_regression.py`.

## Procedimento padrao
1. Classificar a tarefa: calculo financeiro, contexto da view, grafico, layout ou regressao visual.
2. Localizar fonte de dados e ponto de renderizacao (Service -> View -> Template -> JS/CSS).
3. Alterar primeiro a camada de origem (normalmente Service) e depois propagar para UI.
4. Validar coerencia entre valor calculado, template exibido e tooltip/formatacao do grafico.
5. Executar checagens de regressao funcional e visual.

## Mapa rapido de arquivos
- Rotas: `dashboard/urls.py`
- View: `dashboard/views.py`
- Template: `dashboard/templates/dashboard/painel.html`
- Calculos: `finance/services/saldo_service.py`
- Script de graficos: `static/js/dashboard.js`
- Estilos do dashboard: `static/css/dashboard.css`
- Regressao visual: `dashboard/visual_regression.py`

## Regras de decisao
### Se a mudanca for de calculo financeiro
- Implementar em `finance/services/saldo_service.py`.
- Manter uso de `Decimal` para calculos monetarios.
- Preservar retorno estavel para consumo da View/Template (chaves e tipos previsiveis).
- Quando houver comparacao com mes anterior, tratar divisor zero retornando `None` para percentual.

### Se a mudanca for de composicao de dados do painel
- Ajustar `dashboard/views.py` para injetar novos campos no contexto.
- Evitar regra de negocio pesada na View; delegar agregacao ao Service.
- Garantir que consultas e listagens respeitem o usuario autenticado.

### Se a mudanca for em graficos
- Atualizar contrato de dados em `SaldoService` e consumo em `static/js/dashboard.js` em conjunto.
- Manter serializacao segura no template usando `json_script`.
- Validar estados sem dados (`labels` vazio) para nao quebrar renderizacao.

### Se a mudanca for de layout/UX
- Priorizar ajuste de estrutura em `dashboard/templates/dashboard/painel.html`.
- Usar `static/css/dashboard.css` para responsividade e consistencia visual dos cards/paineis.
- Preservar legibilidade de valores financeiros e contraste dos badges de variacao.

### Se a mudanca envolver estabilidade visual
- Validar com suite de regressao em `dashboard/visual_regression.py`.
- Revisar screenshots por breakpoint (mobile, tablet, desktop).
- Atualizar baseline apenas quando a alteracao visual for intencional.

## Checklist de implementacao
1. Confirmar requisito e impacto em KPI, grafico, layout ou regressao visual.
2. Ajustar camada de dados (Service/Repository) quando houver regra/calculo.
3. Atualizar View para expor o contexto necessario ao template.
4. Sincronizar Template e JS com o contrato de dados final.
5. Ajustar CSS para comportamento responsivo e estados vazios.
6. Revisar formatacao de moeda, sinais de variacao e mensagens ao usuario.
7. Executar testes relevantes e validar o fluxo completo do dashboard.

## Checklist de qualidade (Definition of Done)
- KPIs batem com os dados de origem e nao apresentam erros de arredondamento relevantes.
- Grafico de linha, donut e barras renderizam sem erro para cenarios com e sem dados.
- Contrato de dados entre Service, Template e JS esta consistente.
- Layout permanece responsivo em mobile, tablet e desktop.
- Nao ha vazamento de dados entre usuarios.
- Regressao visual foi validada (baseline atualizado somente quando necessario).

## Comandos uteis
```bash
python manage.py test dashboard
python manage.py test dashboard.visual_regression
python manage.py runserver
```

## Prompts de exemplo
- "/dashboard adicionar KPI de ticket medio mensal com variacao percentual"
- "/dashboard ajustar grafico de despesas por categoria para estado sem dados"
- "/dashboard refatorar layout dos cards para melhorar responsividade em tablet"
- "/dashboard revisar inconsistencia entre resumo mensal e grafico de linha"

