---
description: "Implementar nova feature seguindo arquitetura em camadas, clean code e padroes do projeto"
argument-hint: "Descreva a feature: ex. 'CRUD de metas financeiras com listagem HTMX' ou 'novo filtro de período nos lançamentos'"
agent: "agent"
---

# Implementar Feature

Implemente a feature descrita abaixo seguindo rigorosamente a arquitetura e os padroes deste projeto.

## Descricao da feature

{{input}}

---

## Arquitetura obrigatoria

Toda feature segue o fluxo em camadas, sem pular etapas:

```
Request → View → Form (validacao) → Service (regra de negocio) → Repository (ORM) → Response
```

### 1. Repository (acesso a dados)

- Unica camada que toca o ORM.
- Herda de `BaseRepository` ([core/bases/repositories.py](core/bases/repositories.py)).
- Todos os metodos sao `@classmethod` (stateless).
- Exige `user` explicitamente em queries e mutacoes.
- Filtros, `select_related`, `prefetch_related` e agregacoes ficam aqui.

Referencia: [finance/repositories/categoria_repository.py](finance/repositories/categoria_repository.py)

### 2. Service (regra de negocio)

- Herda de `BaseService` ([core/bases/services.py](core/bases/services.py)).
- Recebe `request` no `__init__` e opera com `self.user`.
- Delega persistencia ao Repository — nao usa ORM diretamente.
- Validacoes de dominio (ex: bloqueio de exclusao por dependencias) ficam aqui.

Referencia: [finance/services/categoria_service.py](finance/services/categoria_service.py)

### 3. Form (validacao de entrada)

- Recebe `user=` via `__init__` (injetado pela view base).
- Pode receber `instance=` para edicao.
- Validacoes de campo e unicidade por usuario ficam aqui.
- Nao contem regra de negocio — apenas validacao de entrada.

Referencia: [finance/forms.py](finance/forms.py)

### 4. View (coordenacao HTTP)

- Usa as views base de [core/bases/views.py](core/bases/views.py):
  - `BaseServiceListView` para listagens (com HTMX).
  - `BaseServiceCreateView` / `BaseServiceUpdateView` para formularios.
  - `BaseServiceDeleteView` para exclusao.
  - `BaseTemplateView` para paginas simples.
- Usa mixins de [core/mixins.py](core/mixins.py):
  - `AppLoginRequiredMixin` para autenticacao.
  - `FlashMessageMixin` para feedback.
  - `HtmxRequestMixin` para dual HTMX/normal.
  - `ServiceMixin` / `ServiceObjectMixin` para acesso ao service.
- Nao contem regra de negocio nem ORM direto.

Referencia: [finance/views.py](finance/views.py)

### 5. Template

- Estende os templates base de `templates/` (nao duplicar markup):
  - `base_formulario.html` para formularios autenticados.
  - `base_list.html` para listagens.
  - `base.html` para paginas gerais.
- Usa blocos existentes: `title`, `page_title`, `content`, `extra_css`, `extra_js`.
- Partials HTMX em `partials/` para render parcial de listagens.
- Nao contem regra de negocio.

---

## Procedimento de implementacao

Execute na seguinte ordem:

1. **Model** — Criar/ajustar modelo herdando de `BaseModel` se necessario.
2. **Repository** — Criar repository herdando de `BaseRepository`.
3. **Service** — Criar service herdando de `BaseService`, com validacoes de dominio.
4. **Form** — Criar form com `user=` no `__init__`, validacoes de campo.
5. **View** — Criar views usando as bases do core.
6. **URLs** — Registrar rotas no `urls.py` do app.
7. **Templates** — Criar templates estendendo as bases, com partials HTMX se listagem.
8. **Testes** — Criar testes cobrindo caminho feliz e erros esperados.

---

## Regras inviolaveis

- Escopo por usuario autenticado em todas as operacoes (list, create, update, delete).
- Soft delete via `BaseModel` preservado — nunca usar `hard_delete` sem justificativa.
- HTMX: partial render para listagens, `HX-Redirect` para sucesso com navegacao.
- Request normal: redirect HTTP padrao (302).
- Flash messages para feedback de sucesso e erro.
- Nenhum template base pode ser modificado.

---

## Checklist final

Antes de concluir, valide:

- [ ] Fluxo `View → Form → Service → Repository → ORM` respeitado.
- [ ] Regra de negocio centralizada no Service.
- [ ] ORM encapsulado no Repository.
- [ ] Escopo por usuario autenticado preservado em todas as operacoes.
- [ ] Soft delete / restore funcionando corretamente.
- [ ] Templates estendem bases sem duplicacao.
- [ ] HTMX e request normal funcionam com resposta correta.
- [ ] Mensagens de sucesso e erro exibidas corretamente.
- [ ] Codigo limpo, sem logica morta, sem comentarios obvios.
