---
description: "Use quando alterar fluxos de account: cadastro, login, logout, perfil e configuracoes com Form -> View -> Service -> Repository -> ORM."
applyTo:
  - "account/**"
  - "account/templates/account/**"
---

# Instrucoes do modulo account

## Objetivo
- Garantir fluxo consistente de autenticacao e perfil sem quebrar separacao de camadas.
- Preservar seguranca e ownership do usuario autenticado.

## Arquitetura obrigatoria
1. View recebe request e coordena resposta HTTP.
2. Form valida entrada e mensagens de erro.
3. Service aplica regra de negocio.
4. Repository encapsula persistencia e consultas.
5. ORM fica dentro do Repository.

## Regras do modulo
- Nao implementar regra de negocio complexa na View.
- Nao acessar ORM direto na View.
- Nao acessar ORM direto no Service quando houver Repository.
- Em cadastro, manter consistencia entre criacao de User e Perfil.
- Em logout, manter fluxo por POST.
- Em telas publicas (login/cadastro), usar mixin de acesso anonimo.
- Em telas autenticadas (perfil/configuracoes), exigir login.

## Pontos de implementacao
- Formularios e validacoes: account/forms.py
- Regra de negocio: account/services/auth_service.py
- Persistencia: account/repositories/user_repository.py
- Fluxo HTTP e redirecionamentos: account/views.py
- Rotas namespaced: account/urls.py

## Checklist rapido
1. Fluxo Form -> Service -> Repository aplicado.
2. Erros de validacao retornam no Form com mensagem clara.
3. Nao existe acesso indevido a dados de outro usuario.
4. Login, logout, cadastro e perfil continuam funcionais.

