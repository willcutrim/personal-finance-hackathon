from core.bases.services import BaseService
from finance.repositories.lancamento_repository import LancamentoRepository


class LancamentoService(BaseService):
    repository_class = LancamentoRepository

    def create(self, **data):
        categoria = data.get('categoria')
        if categoria:
            data['tipo'] = categoria.tipo
        return self.repository_class.create(user=self.user, **data)

    def update(self, instance, **data):
        categoria = data.get('categoria', instance.categoria)
        data['tipo'] = categoria.tipo
        return self.repository_class.update(instance, user=self.user, **data)

    def list(self, include_deleted=False, **filters):
        return self.repository_class.list(
            include_deleted=include_deleted,
            user=self.user,
            **filters,
        )
