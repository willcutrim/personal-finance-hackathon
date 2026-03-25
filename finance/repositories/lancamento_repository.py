from decimal import Decimal

from django.db.models import Sum

from core.bases.repositories import BaseRepository
from finance.models import Lancamento, TipoChoices


class LancamentoRepository(BaseRepository):
    model = Lancamento

    @classmethod
    def get_queryset(cls, include_deleted=False, user=None):
        qs = cls._get_manager(include_deleted=include_deleted).select_related('categoria')
        if user is not None:
            qs = qs.filter(user=user)
        return qs

    @classmethod
    def list(cls, include_deleted=False, user=None, **filters):
        # Extrair filtros de intervalo de data antes de chamar filter(**filters)
        data_inicio = filters.pop('data_inicio', None)
        data_fim = filters.pop('data_fim', None)
        qs = cls.get_queryset(include_deleted=include_deleted, user=user).filter(**filters)
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        return qs

    @classmethod
    def create(cls, user=None, **data):
        data['user'] = user
        return cls.model.objects.create(**data)

    @classmethod
    def saldo_por_tipo(cls, user):
        resultado = (
            cls.get_queryset(user=user)
            .values('tipo')
            .annotate(total=Sum('valor'))
        )
        totais = {row['tipo']: row['total'] or Decimal('0') for row in resultado}
        receitas = totais.get(TipoChoices.RECEITA, Decimal('0'))
        despesas = totais.get(TipoChoices.DESPESA, Decimal('0'))
        return {
            'total_receitas': receitas,
            'total_despesas': despesas,
            'saldo': receitas - despesas,
        }

    @classmethod
    def totais_por_categoria(cls, user, tipo):
        return (
            cls.get_queryset(user=user)
            .filter(tipo=tipo)
            .values('categoria__nome')
            .annotate(total=Sum('valor'))
            .order_by('-total')
        )

    @classmethod
    def totais_mensais(cls, user, ano):
        from django.db.models.functions import ExtractMonth
        return (
            cls.get_queryset(user=user)
            .filter(data__year=ano)
            .annotate(mes=ExtractMonth('data'))
            .values('mes', 'tipo')
            .annotate(total=Sum('valor'))
            .order_by('mes')
        )

    @classmethod
    def ultimos(cls, user, limit=5):
        return cls.get_queryset(user=user)[:limit]
