from django.core.exceptions import ValidationError

from core.bases.services import BaseService
from finance.repositories.categoria_repository import CategoriaRepository


class CategoriaService(BaseService):
    repository_class = CategoriaRepository

    def delete(self, instance):
        if CategoriaRepository.has_lancamentos_ativos(instance):
            raise ValidationError(
                'Não é possível excluir esta categoria pois existem lançamentos vinculados a ela.'
            )
        return super().delete(instance)

    def list_por_tipo(self, tipo):
        return self.repository_class.list(user=self.user, tipo=tipo)
