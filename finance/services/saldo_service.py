from decimal import Decimal, ROUND_HALF_UP

from finance.models import TipoChoices
from finance.repositories.lancamento_repository import LancamentoRepository


class SaldoService:
    """
    Serviço utilitário stateless para cálculos financeiros de dashboard.
    Recebe o user como argumento — não herda BaseService.
    """

    def __init__(self, user):
        self.user = user

    def calcular_saldo(self):
        return LancamentoRepository.saldo_por_tipo(self.user)

    def resumo_por_categoria(self, tipo=TipoChoices.DESPESA):
        rows = LancamentoRepository.totais_por_categoria(self.user, tipo)
        return {
            'labels': [row['categoria__nome'] for row in rows],
            'valores': [float(row['total']) for row in rows],
        }

    def resumo_mensal(self, ano):
        rows = list(LancamentoRepository.totais_mensais(self.user, ano))
        meses = list(range(1, 13))
        receitas_por_mes = {row['mes']: float(row['total']) for row in rows if row['tipo'] == TipoChoices.RECEITA}
        despesas_por_mes = {row['mes']: float(row['total']) for row in rows if row['tipo'] == TipoChoices.DESPESA}
        return {
            'labels': [_nome_mes(m) for m in meses],
            'receitas': [receitas_por_mes.get(m, 0) for m in meses],
            'despesas': [despesas_por_mes.get(m, 0) for m in meses],
        }

    def ultimos_lancamentos(self, limit=5):
        return LancamentoRepository.ultimos(self.user, limit=limit)

    def calcular_percentual_economia(self, total_receitas, total_despesas):
        if not total_receitas:
            return None
        economia = total_receitas - total_despesas
        if economia <= 0:
            return None
        percentual = (economia / total_receitas * 100).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        return percentual


def _nome_mes(numero):
    nomes = [
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',
    ]
    return nomes[numero - 1]
