---
name: account
description: 'WORKFLOW SKILL para o modulo account (cadastro, login, logout, perfil e configuracoes) em Django com camadas Form + View + Service + Repository. Use para criar/ajustar fluxos de autenticacao, validacoes de cadastro, telas account e regras de usuario/perfil com checagens de regressao.'
argument-hint: 'Descreva a tarefa no account: ex. "adicionar validacao no cadastro" ou "criar edicao de perfil"'
user-invocable: true
---

# Account Module Workflow

## Quando usar
- Implementar ou corrigir fluxo de cadastro, login, logout, perfil ou configuracoes.
- Alterar validacoes de usuario, e-mail, senha ou mensagens de formulario.
- Ajustar regras no Service ou persistencia no Repository do app account.
- Criar testes para evitar regressao no fluxo de autenticacao.

## Contexto do projeto
- Stack: Django com arquitetura em camadas (Form, View, Service, Repository).
- Namespace de rotas: `accounts`.
- Fluxos atuais: cadastro com criacao de `User` + `Perfil`, login, logout via POST, paginas de perfil e configuracoes.

## Procedimento padrao
1. Identificar o tipo de tarefa no account.
2. Localizar os pontos de entrada e saida do fluxo (URL, View, Form, Service, Repository).
3. Aplicar mudanca na camada correta sem quebrar separacao de responsabilidades.
4. Validar comportamento funcional (sucesso e erro) e mensagens ao usuario.
5. Executar checagens minimas de regressao.

## Mapa rapido de arquivos
- Rotas: `account/urls.py`
- Views: `account/views.py`
- Formularios: `account/forms.py`
- Service: `account/services/auth_service.py`
- Repository: `account/repositories/user_repository.py`
- Modelo de perfil: `account/models.py`
- Templates: `account/templates/account/`

## Regras de decisao
### Se a mudanca for de tela/UX de formulario
- Preferir `account/forms.py` para labels, placeholders e validacoes de campo.
- Ajustar `account/templates/account/*.html` somente para apresentacao.

### Se a mudanca for de regra de negocio
- Implementar em `account/services/auth_service.py`.
- Manter transacao atomica quando envolver criacao de `User` e `Perfil`.
- Levantar `ValidationError` com mensagens claras para a camada de View.

### Se a mudanca for de persistencia
- Implementar em `account/repositories/user_repository.py`.
- Manter metodos pequenos, sem regra de negocio complexa.
- Para senha, manter criacao via `create_user`.

### Se a mudanca for de navegacao/autenticacao
- Ajustar `account/views.py` e `account/urls.py`.
- Respeitar mixins ja usados (`AnonymousOnlyMixin`, `AppLoginRequiredMixin`, `FlashMessageMixin`).
- Para logout, preservar metodo POST.

## Checklist de implementacao
1. Confirmar impacto do requisito no fluxo: cadastro, login, logout, perfil ou configuracoes.
2. Atualizar primeiro a camada principal da mudanca (Form, Service, Repository ou View).
3. Ajustar chamadas entre camadas sem duplicar validacoes desnecessariamente.
4. Garantir mensagens de feedback para sucesso/erro.
5. Revisar rotas e redirecionamentos esperados.
6. Atualizar template apenas se houver mudanca visual/semantica necessaria.
7. Adicionar ou atualizar testes no app account.

## Checklist de qualidade (Definition of Done)
- Fluxo principal funciona ponta a ponta.
- Casos de erro relevantes estao tratados (ex.: e-mail duplicado no cadastro).
- Nao ha regra de negocio escondida em View ou Template.
- Nao ha acesso direto ao banco na camada de View.
- Rotas e nomes (`accounts:*`) permanecem consistentes.
- Testes do account (ou relacionados) cobrem o novo comportamento.

## Prompts de exemplo
- "/account adicionar validacao de username no cadastro sem quebrar login"
- "/account criar fluxo de edicao de perfil com formulario e service"
- "/account revisar login/logout e apontar riscos de seguranca e regressao"

