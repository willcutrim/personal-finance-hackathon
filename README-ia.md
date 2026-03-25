# 🤖 Configuração de IA — GitHub Copilot

Este projeto usa GitHub Copilot com configurações customizadas para garantir que o agente siga a arquitetura em camadas e os padrões do projeto automaticamente.

---

## Estrutura `.github/`

```
.github/
├── copilot-instructions.md   # regras globais aplicadas em todo contexto
├── instructions/             # regras automáticas por módulo (sempre ativas)
│   ├── account.instructions.md
│   ├── finance.instructions.md
│   └── dashboard.instructions.md
├── skills/                   # workflows detalhados invocados sob demanda
│   ├── account/SKILL.md
│   ├── finance/SKILL.md
│   └── dashboard/SKILL.md
└── prompts/                  # prompts reutilizáveis para tarefas estruturadas
    ├── criar_nova_feature.prompt.md
    ├── configurar_app_novo.prompt.md
    └── criar_templates_htmx.prompt.md
```

---

## Responsabilidades

**`copilot-instructions.md`** — regras arquiteturais globais sempre injetadas: fluxo `View → Form → Service → Repository → ORM`, soft delete, mixins obrigatórios e comportamento HTMX. O agente nunca ignora essas regras.

**`instructions/`** — complementam as regras globais para um módulo específico. São carregadas automaticamente quando o arquivo aberto pertence ao app correspondente (via `applyTo`). Dispensam invocação manual.

**`skills/`** — workflows completos com mapa de arquivos, procedimento passo a passo e checklist de regressão. Ativados explicitamente quando a tarefa é maior ou mais crítica — garantem que o agente siga o procedimento correto do início ao fim, não só as regras.

> **Diferença prática:** instructions *restringem* o comportamento do agente. Skills *guiam* o agente por um procedimento completo.

---

## Prompts disponíveis

Use os prompts do painel "Prompts" do Copilot Chat ou com `/` no chat:

| Prompt | Quando usar |
|---|---|
| `criar_nova_feature` | Implementar qualquer feature nova do zero seguindo todas as camadas. Passe uma descrição da feature e o agente entrega View, Form, Service, Repository, templates e URLs. |
| `configurar_app_novo` | Configuração inicial para início de desenvolvimento de um app Django novo no padrão do projeto. Informe nome do app, contexto de negócio e entidades principais. |
| `criar_templates_htmx` | Criar ou adaptar telas com HTMX: listas parciais, modais de criação/edição/exclusão sem reload. Informe app, modelo e tipo de operação desejada. |

### Por que usar os prompts em vez de pedir diretamente?

Os prompts já encapsulam todas as restrições arquiteturais, os arquivos de referência e o formato de entrega esperado. Pedir sem o prompt exige repetir esse contexto manualmente — e aumenta a chance do agente desviar dos padrões do projeto.