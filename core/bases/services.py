class BaseService:
    """
    Service base para operações de domínio.

    Responsabilidade: orquestrar regras de negócio e delegar
    persistência ao repository. Não acessa o ORM diretamente.

    Como usar:
        class CategoriaService(BaseService):
            repository_class = CategoriaRepository

    O service é instanciado com o `request` atual:
        service = CategoriaService(request)
        service.list()          # já usa self.user internamente
        service.create(**data)  # já injeta self.user

    Nas views, prefira usar `get_service()` (do ServiceMixin) que
    instancia e cacheia automaticamente o service para a requisição.

    O que a subclasse pode sobrescrever:
        - `list` — para filtros adicionais de domínio
        - `create` / `update` — para validações de negócio antes de persistir
        - `delete` — para validações antes de remover (ex: dependências)
    """

    repository_class = None

    def __init__(self, request):
        """
        Recebe o request da view atual.
        Armazena o usuário autenticado em self.user para uso interno,
        evitando que cada chamada precise passar user= manualmente.
        """
        self.request = request
        self.user = request.user

    def get_queryset(self, include_deleted=False):
        """Retorna o queryset base filtrado pelo usuário autenticado."""
        return self.repository_class.get_queryset(include_deleted=include_deleted, user=self.user)

    def list(self, include_deleted=False, **filters):
        """Lista registros do usuário autenticado com filtros opcionais."""
        return self.repository_class.list(include_deleted=include_deleted, user=self.user, **filters)

    def get_by_id(self, object_id, include_deleted=False):
        """Busca um registro pelo id, restrito ao usuário autenticado."""
        return self.repository_class.get_by_id(object_id, include_deleted=include_deleted, user=self.user)

    def create(self, **data):
        """Cria um novo registro associado ao usuário autenticado."""
        return self.repository_class.create(user=self.user, **data)

    def update(self, instance, **data):
        """Atualiza os campos fornecidos de um registro existente."""
        return self.repository_class.update(instance, user=self.user, **data)

    def delete(self, instance):
        """Remove (soft-delete) um registro. Subclasses podem adicionar validações."""
        return self.repository_class.delete(instance)

    def restore(self, instance):
        """Restaura um registro soft-deleted."""
        return self.repository_class.restore(instance)

    def hard_delete(self, instance):
        """Delete físico permanente. Use com cautela."""
        return self.repository_class.hard_delete(instance)
