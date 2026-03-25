from core.bases.repositories import BaseRepository
from finance.models import Categoria


class CategoriaRepository(BaseRepository):
    model = Categoria

    @classmethod
    def get_queryset(cls, include_deleted=False, user=None):
        qs = cls._get_manager(include_deleted=include_deleted).all()
        if user is not None:
            qs = qs.filter(user=user)
        return qs

    @classmethod
    def list(cls, include_deleted=False, user=None, **filters):
        return cls.get_queryset(include_deleted=include_deleted, user=user).filter(**filters)

    @classmethod
    def create(cls, user=None, **data):
        data['user'] = user
        return cls.model.objects.create(**data)

    @classmethod
    def has_lancamentos_ativos(cls, categoria):
        return categoria.lancamentos.exists()
