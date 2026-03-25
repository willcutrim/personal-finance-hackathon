# 💰 Personal Finance — Gestão de Finanças Pessoais

Sistema web para controle de finanças pessoais. Registre receitas e despesas, organize por categorias e acompanhe seu saldo no dashboard — tudo isolado por usuário.

**Stack:** Python 3.13+ · Django 6 · HTMX · SQLite · Chart.js

---

## Tecnologias

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | ≥ 3.13 | Linguagem principal |
| Django | 6.0.3 | Framework web (backend, ORM, templates) |
| django-htmx | 1.27.0 | Middleware e utilitários para requisições HTMX |
| SQLite | — | Banco de dados embutido (zero configuração) |
| Pillow | 12.1.1 | Suporte a imagens (upload de avatar/perfil) |
| Playwright | 1.58.0 | Testes de regressão visual |
| Chart.js | (CDN) | Gráficos interativos no dashboard |
| HTMX | (CDN) | Interatividade no frontend sem JavaScript complexo |

---

## Pré-requisitos

- **Python 3.13+** instalado e disponível no PATH
- **pip** (gerenciador de pacotes do Python)
- **Git** para clonar o repositório

---

## Instalação e Execução

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd personal-finance-hackathon

# 2. Criar e ativar o ambiente virtual
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrações do banco de dados
python manage.py migrate

# 6. Iniciar o servidor de desenvolvimento
python manage.py runserver
```

Acesse o sistema em **http://localhost:8000**. Após o login, você será redirecionado ao **Login**.

---

## Estrutura do Projeto

```
personal-finance-hackathon/
│
├── personal_finance_hackathon/   # Configuração do projeto Django
│
├── core/                         # Módulo de infraestrutura e bases reutilizáveis
│   ├── bases/
│   │   ├── models.py             # BaseModel com soft delete
│   │   ├── services.py           # BaseService (regras de negócio)
│   │   ├── repositories.py       # BaseRepository (acesso a dados)
│   │   └── views.py              # Views base (List, Create, Update, Delete)
│   └── mixins.py                 # Mixins de autenticação, HTMX e flash messages
│
├── account/                      # Módulo de autenticação e perfil
│
├── finance/                      # Módulo de categorias e lançamentos
│
├── dashboard/                    # Módulo do painel principal
│
├── templates/                    # Templates globais e base
│   ├── base.html                 # Layout principal
│   ├── base_formulario.html      # Layout de formulários (autenticado)
│   ├── base_list.html            # Layout de listagens
│   ├── includes/                 # Componentes reutilizáveis (sidebar, topbar, alerts)
│   └── partials/                 # Fragmentos para HTMX
│
├── static/                       # Arquivos estáticos (.js/.css)
│   ├── css/                      # Estilos (base, components, dashboard, layout)
│   └── js/                       # Scripts (base, dashboard, dropdown, sidebar)
│
└── .docs/                        # Diagramas e documentação auxiliar
```

---

## Arquitetura em Camadas

O sistema segue uma arquitetura em camadas obrigatória, onde cada camada tem responsabilidade bem definida e **não é permitido pular camadas**.

### Fluxo de Execução

```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────────┐     ┌───────┐
│  View   │────▸│  Form    │────▸│  Service  │────▸│  Repository  │────▸│  ORM  │
│ (HTTP)  │     │(validação)│    │ (negócio) │     │  (dados)     │     │       │
└─────────┘     └──────────┘     └───────────┘     └──────────────┘     └───────┘
```

| Camada | Responsabilidade |
|---|---|
| **View** | Coordena o fluxo HTTP: recebe request, monta contexto, retorna response/redirect. Trata filtros e parâmetros de querystring. |
| **Form** | Valida entrada do usuário, normaliza dados e gera mensagens de erro de campo. |
| **Service** | Camada central de regra de negócio. Orquestra operações de CRUD, validações de domínio e escopo por usuário autenticado. Instanciado com o `request` atual. |
| **Repository** | Única camada que acessa o ORM. Expõe métodos claros (`list`, `get_by_id`, `create`, `update`, `delete`) e encapsula querysets, filtros e agregações. Stateless (`@classmethod`). |

---

### BaseModel e Soft Delete

Todas as entidades de domínio herdam de `BaseModel` (`core/bases/models.py`), que implementa o padrão de **soft delete**:

```python
class BaseModel(models.Model):
    criado_em    = DateTimeField(auto_now_add=True)
    atualizado_em = DateTimeField(auto_now=True)
    deletado_em  = DateTimeField(null=True, blank=True)  # soft delete
```

**Managers disponíveis:**

| Manager | Retorna |
|---|---|
| `Model.objects` | Apenas registros **ativos** (`deletado_em IS NULL`) |
| `Model.all_objects` | **Todos** os registros (ativos + deletados) |

**Operações de exclusão:**

| Método | Comportamento |
|---|---|
| `instance.delete()` | Marca `deletado_em` com timestamp atual (soft delete) |
| `instance.restore()` | Remove a marcação de `deletado_em` (reativa o registro) |
| `instance.hard_delete()` | Remove fisicamente do banco de dados |

---

### BaseService

`BaseService` (`core/bases/services.py`) é a classe base para todos os services do sistema.

- **Instanciado com o `request`**, armazena `self.user` para uso em todas as operações.
- Delega persistência ao **Repository** — nunca acessa o ORM diretamente.
- Fornece métodos padrão: `list()`, `get_by_id()`, `create()`, `update()`, `delete()`, `restore()`.

```python
service = CategoriaService(request)
service.list()           # já filtra pelo usuário autenticado
service.create(**data)   # já associa ao usuário autenticado
```

---

### BaseRepository

`BaseRepository` (`core/bases/repositories.py`) é a classe base para todos os repositories.

- **Stateless** — todos os métodos são `@classmethod` (não carrega contexto de request).
- Única camada que toca o **ORM Django**.
- Fornece métodos padrão: `get_queryset()`, `list()`, `get_by_id()`, `create()`, `update()`, `delete()`.
- Subclasses sobrescrevem `get_queryset()` para adicionar filtros fixos (ex.: `filter(user=user)`).

---

### Views Base

O módulo `core/bases/views.py` fornece views base que combinam autenticação, HTMX, service e flash messages:

| View Base | Uso |
|---|---|
| `BaseTemplateView` | Páginas simples sem CRUD (dashboard, perfil, configurações) |
| `BaseServiceListView` | Listagens com service, paginação, filtros e suporte HTMX (partial template) |
| `BaseServiceCreateView` | Formulários de criação via service com `user` injetado automaticamente |
| `BaseServiceUpdateView` | Formulários de edição via service com instância carregada por `pk` |
| `BaseServiceDeleteView` | Exclusão com confirmação, tratamento automático de `ValidationError` e flash message |

---

### Mixins

O módulo `core/mixins.py` fornece mixins reutilizáveis:

| Mixin | Finalidade |
|---|---|
| `AppLoginRequiredMixin` | Exige autenticação com `login_url` padronizado do projeto |
| `AnonymousOnlyMixin` | Redireciona usuários já logados (usado em login/cadastro) |
| `FlashMessageMixin` | Envia mensagens de sucesso/erro via Django messages framework |
| `HtmxRequestMixin` | Detecta requisição HTMX e fornece `redirect_response()` dual (HTTP 302 ou HX-Redirect 204) |
| `ServiceMixin` | Instancia e cacheia o service da view (via `get_service()`) |
| `ServiceObjectMixin` | Adiciona `get_object()` com lookup por `pk` via service, com proteção cross-user (Http404) |

---

## Módulos do Sistema

### Account — Autenticação e Perfil

O módulo `account` gerencia todo o ciclo de vida do usuário no sistema.

#### Decisões de Negócio

- **Unicidade**: username e email são validados como únicos no `AuthService` antes da criação.
- **Perfil automático**: ao cadastrar, o sistema cria um `Perfil` (modelo `1:1` com `User`) dentro de uma transação atômica — garante consistência.
- **Proteção de acesso**: telas de login e cadastro usam `AnonymousOnlyMixin` (usuários já logados são redirecionados ao Dashboard). Telas de perfil e configurações exigem `AppLoginRequiredMixin`.
- **Validação de senha**: utiliza os validadores padrão do Django (`MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`, `UserAttributeSimilarityValidator`).
- **Email em edição de perfil**: validação de unicidade cross-user (não permite email já usado por outro usuário).

---

### Finance — Categorias e Lançamentos

O módulo `finance` é o coração do sistema, responsável pela gestão de categorias e lançamentos financeiros.

#### Decisões de Negócio

- **Tipo inferido**: o tipo do lançamento (`RECEITA`/`DESPESA`) é definido automaticamente pela categoria selecionada — o usuário não escolhe o tipo diretamente no lançamento.
- **Proteção de exclusão**: uma categoria com lançamentos ativos **não pode ser excluída**. O `CategoriaService.delete()` levanta `ValidationError` que é exibida como flash message.
- **FK com PROTECT**: a FK `categoria` no `Lancamento` usa `on_delete=PROTECT`, garantindo integridade referencial a nível de banco.
- **Ownership**: todas as operações (listar, criar, editar, excluir) são filtradas pelo `user` autenticado — um usuário **jamais** acessa dados de outro.
- **Valor positivo**: validação no formulário impede valores menores ou iguais a zero.
- **Formulários em modal**: criação e edição de lançamentos acontecem em modais HTMX. Após sucesso, o evento `lancamentoChanged` é disparado para recarregar a listagem.
- **Filtros com paginação**: filtros por tipo, categoria e intervalo de datas funcionam em conjunto com a paginação, preservando o estado via querystring.


---

### Dashboard — Painel e KPIs

O módulo `dashboard` exibe um painel financeiro completo com indicadores, gráficos e lançamentos recentes.

#### Decisões de Negócio

- **SaldoService separado**: não herda de `BaseService` — é um serviço utilitário stateless que recebe `user`, `data_inicio` e `data_fim` diretamente. Essa decisão evita acoplar cálculos de agregação ao ciclo de vida request/service padrão.
- **Cálculos com Decimal**: todos os valores monetários usam `Decimal` para evitar erros de ponto flutuante.
- **Agregações no Repository**: os cálculos de `saldo_por_tipo`, `totais_por_categoria` e `totais_mensais` são feitos diretamente no banco via `Sum`, `annotate` e `values` — otimizando performance ao evitar processamento em Python.
- **Escopo do usuário**: todos os dados exibidos são filtrados pelo `user` autenticado — não há vazamento de dados entre usuários.

---

## Templates Base

O projeto utiliza templates base em `templates/` que os módulos estendem:

| Template | Uso |
|---|---|
| `base.html` | Layout principal para páginas autenticadas. Inclui sidebar, topbar, alerts e blocos `content`, `extra_css`, `extra_js`. |
| `base_public.html` | Layout para páginas públicas (login, cadastro). Sem sidebar/topbar. |
| `base_list.html` | Layout para listagens. Suporte a `list_partial_template` para HTMX, paginação e empty state. |

**Blocos reutilizáveis**: `title`, `page_title`, `page_subtitle`, `content`, `extra_css`, `extra_js`.

**Includes globais**: `includes/alerts.html`, `includes/page_header.html`, `includes/sidebar.html`, `includes/topbar.html`, `includes/pagination.html`, `includes/empty_state.html`.


---

## Documentação Auxiliar

Diagramas e documentos adicionais que serviram de base para a implementação estão disponíveis na pasta [.docs/](.docs/), projetados no [Excalidraw](https://excalidraw.com).