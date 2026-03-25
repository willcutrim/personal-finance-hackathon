class BaseRepository:
    """
    Repositório base para operações de banco de dados.

    Responsabilidade: única camada que toca o ORM. Não contém
    regras de negócio — apenas traduz chamadas em queries.

    Como usar:
        class MinhaRepository(BaseRepository):
            model = MeuModel

    O que a subclasse pode sobrescrever:
        - `get_queryset` — para aplicar filtros fixos (ex: user, tenant)
        - `list` — para adicionar ordenação específica
        - `create` / `update` — para setar campos automáticos (ex: user)

    Nota: todos os métodos são @classmethod porque o repositório é
    stateless — não carrega contexto de request entre chamadas.
    """

    model = None

    @classmethod
    def _get_manager(cls, include_deleted=False):
        """Retorna o manager correto: ativos ou todos (incluindo soft-deleted)."""
        if include_deleted and hasattr(cls.model, "all_objects"):
            return cls.model.all_objects
        return cls.model.objects

    @classmethod
    def get_queryset(cls, include_deleted=False, user=None):
        """
        Queryset base. Subclasses devem sobrescrever para adicionar
        filtros fixos (ex: .filter(user=user)).
        """
        return cls._get_manager(include_deleted=include_deleted).all()

    @classmethod
    def list(cls, include_deleted=False, user=None, **filters):
        """Lista registros aplicando filtros dinâmicos opcionais."""
        return cls.get_queryset(include_deleted=include_deleted, user=user).filter(**filters)

    @classmethod
    def get_by_id(cls, object_id, include_deleted=False, user=None):
        """Busca um registro pelo id. Retorna None se não encontrado."""
        return cls.get_queryset(include_deleted=include_deleted, user=user).filter(id=object_id).first()

    @classmethod
    def create(cls, user=None, **data):
        """Cria e persiste um novo registro. Injeta user se fornecido."""
        if user is not None:
            data.setdefault("user", user)
        return cls.model.objects.create(**data)

    @classmethod
    def update(cls, instance, user=None, **data):
        """
        Atualiza apenas os campos fornecidos em `data` usando
        update_fields para evitar sobrescrita acidental de outros campos.
        """
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(data.keys()))
        return instance

    @classmethod
    def delete(cls, instance):
        """Soft-delete: marca deletado_em (se BaseModel) ou deleta normalmente."""
        instance.delete()
        return instance

    @classmethod
    def restore(cls, instance):
        """Restaura um registro soft-deleted."""
        if hasattr(instance, "restore"):
            instance.restore()
        return instance

    @classmethod
    def hard_delete(cls, instance):
        """Delete físico permanente do banco de dados."""
        if hasattr(instance, "hard_delete"):
            instance.hard_delete()
        else:
            instance.delete()
