---
description: "Configura app novo ou copiado no padrao View -> Form/Filters -> Service -> Repositorys -> ORM, com URLs, templates e CRUD base"
name: "Configurar App Novo"
argument-hint: "Informe o nome do app e o objetivo (ex.: contas a pagar, metas, assinaturas)"
agent: "agent"
---

Quero que voce configure um app Django novo ou copiado neste projeto seguindo o padrao arquitetural oficial:

1. View
2. Form/Filters
3. Service
4. Repositorys
5. ORM

Objetivo do app solicitado pelo usuario:
- Nome do app: {{nome_do_app}}
- Contexto de negocio: {{objetivo_do_app}}
- Entidades principais: {{entidades_principais}}

Regras obrigatorias:
- Nao pular camadas.
- Nao colocar regra de negocio em template.
- Nao usar ORM direto na View.
- Não inflar conteudo da View. Sugerir ao usuário alternativas inteligentes em caso de contextos grandes.
- Nao usar ORM direto no Service quando houver Repository.
- Preservar escopo por usuario autenticado em todas as operacoes.
- Manter compatibilidade com HTMX quando a feature usar listagem parcial.

Entregue implementacao completa e consistente para o app, incluindo:
- Modelos e campos essenciais.
- Forms e filtros.
- Services com regras de negocio.
- Repositorys com consultas/persistencia ORM.
- Views baseadas nas classes do core.
- URLs do app e inclusao no roteamento global quando aplicavel.
- Templates (lista, formulario, confirmacao de delete e parciais HTMX quando necessario).

Checklist tecnico minimo que voce deve aplicar:
1. Estrutura de pastas do app (models, forms, services, repositories, views, urls, templates).
2. Nomes e paths consistentes de classes, funcoes, arquivos e templates.
3. CRUD padrao com o menor numero possivel de customizacoes repetidas.
4. Reaproveitamento de bases/mixins do projeto para list/create/update/delete.
5. Regra de ownership no Service e consultas encapsuladas no Repository.
6. Fluxo HTMX e nao-HTMX valido para listagens e redirecionamentos.
7. Ajustes de admin, migrations e navegacao apenas quando fizer sentido para a feature.

Regra importante sobre indices e desempenho:
- Verifique em runtime quais campos sao usados pelas views, filtros e ordenacoes antes de sugerir indices.
- Nao assumir nomes de campo fixos sem validar no codigo e no modelo real.
- Proponha indices somente para campos efetivamente usados em filtros, joins e ordenacao.
- Para casos como dashboard, considere principalmente recortes por periodo, data, categoria e tipo quando esses campos realmente existirem e forem usados.

Forma de trabalho esperada:
1. Ler estrutura existente do projeto e mapear padroes do modulo semelhante.
2. Validar lacunas com perguntas curtas apenas se bloquear implementacao.
3. Implementar seguindo convencoes atuais do repositorio.
4. Executar checagem de qualidade final com o fluxo em camadas.

Padrao de resposta:
- Mostrar primeiro o que foi criado/alterado.
- Em seguida, listar arquivos por camada (View, Form/Filters, Service, Repository, Templates, URLs).
- Explicar rapidamente onde ficou cada regra de negocio e cada consulta ORM.
- Informar riscos, pendencias e proximos passos objetivos.

Exemplos de uso deste prompt:

Exemplo 1:
- Entrada: "Configurar app de assinaturas com plano, recorrencia mensal e controle por usuario."
- Esperado: CRUD base das entidades, filtros de periodo e status, service com regra de ownership, repository com consultas encapsuladas.

Exemplo 2:
- Entrada: "Copiar padrao do finance para app de metas financeiras com listagem HTMX."
- Esperado: estrutura equivalente a finance, templates de lista e parciais, service chamando repository, sem ORM na view/service.

Exemplo 3:
- Entrada: "Criar app de compromissos financeiros para dashboard mensal."
- Esperado: campos e filtros definidos conforme necessidade real das views; sugestao de indices baseada no uso efetivo de filtros/ordenacao.

# IMPORTANTE
## Não quero que voce produza o app todo do zero, mas sim que voce guie o desenvolvimento. Informe ao usuário no final que os templates do projeto podem ser melhor realizados com o criar_templates_htmx.prompt.md, que tem um foco mais específico em templates e HTMX. 
### Este prompt é para configurar a estrutura geral do app, enquanto o outro é para detalhar os templates.