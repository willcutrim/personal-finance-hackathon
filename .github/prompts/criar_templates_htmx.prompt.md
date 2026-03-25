---
description: "Auxilia a criar tabelas e templates HTMX com formularios em popup sem reload completo, seguindo Forms -> Service -> Repository -> ORM"
name: "Criar Templates HTMX"
argument-hint: "Informe app, modelo e tipo de fluxo HTMX desejado (lista, modal create/edit, delete)"
agent: "agent"
---

Quero que voce me ajude a implementar telas HTMX para novas tabelas no sistema, usando como referencia os padroes de Categorias e Lancamentos.

Foco principal deste prompt:
- Criar ou adaptar templates e fluxo HTMX para CRUD.
- Suportar formularios em popup interativo (modal), com envio sem recarregar a pagina.
- Garantir que a entrada passe por Django Forms, mesmo quando o formulario estiver em parcial HTMX.

Fluxo tecnico obrigatorio:
1. View recebe request e decide resposta completa vs parcial HTMX.
2. Form/Filters valida entrada e normaliza dados.
3. Service aplica regra de negocio e ownership do usuario.
4. Repository executa leitura/escrita e consultas.
5. ORM fica encapsulado no Repository.

Entrada esperada do usuario:
- App alvo: {{app}}
- Modelo(s) alvo: {{modelos}}
- Operacao: {{list|create|update|delete|crud_completo}}
- UX desejada: {{modal_htmx|inline_htmx|misto}}
- Campos obrigatorios e filtros: {{campos_e_filtros}}

O que voce deve entregar:
1. Plano curto de implementacao por camada (View, Form/Filters, Service, Repository, Templates, URLs).
2. Lista de arquivos a criar/alterar e paths corretos.
3. Exemplo de estrutura de templates:
	- template de pagina completa
	- partial de tabela/lista
	- partial de formulario modal
	- partial de mensagens/erros de validacao
4. Exemplo dos atributos HTMX necessarios (hx-get, hx-post, hx-target, hx-swap, hx-trigger) para abrir modal, submeter e atualizar lista.
5. Regras de resposta:
	- sucesso com HTMX: atualizar alvo parcial ou usar HX-Redirect quando houver navegacao
	- erro de form com HTMX: retornar parcial do formulario com erros
	- request normal: manter comportamento HTTP padrao

Regras de qualidade:
- Nao gerar formulario somente de pagina completa quando o requisito for HTMX.
- Nao pular Django Forms em submissao de modal.
- Nao fazer ORM direto em View ou Service.
- Nao assumir campos fixos para filtros e indices.
- Verificar em runtime os campos realmente usados por filtros/ordenacao antes de sugerir indice.
- Priorizar reutilizacao dos templates base e includes globais do projeto.

Padrao de saida da resposta:
1. Resumo do que sera implementado.
2. Arquivos por camada.
3. Trechos de codigo essenciais (somente o necessario).
4. Checklist final de validacao HTMX.

Checklist final HTMX (sempre executar):
1. Modal abre via HTMX sem reload.
2. Submit do form passa por Django Form.
3. Erros de validacao retornam no proprio modal.
4. Sucesso atualiza a lista/tabela alvo sem reload completo.
5. Fluxo nao-HTMX continua funcional.

Exemplo 1:
- Entrada: "App finance, modelo CategoriaExtra, CRUD com modal HTMX".
- Esperado: listagem parcial + modal create/edit + delete com confirmacao + atualizacao da tabela apos submit.

Exemplo 2:
- Entrada: "App finance, modelo LancamentoFuturo, filtros por periodo e tipo".
- Esperado: filtros em Form/Filters, service orquestrando regras, repository com query otimizada, lista HTMX atualizada por filtros.

Exemplo 3:
- Entrada: "App dashboard, tabela auxiliar de metas mensais com popup de cadastro rapido".
- Esperado: formulario modal com validacao por Django Form, retorno parcial em erro e refresh parcial dos cards/lista em sucesso.
