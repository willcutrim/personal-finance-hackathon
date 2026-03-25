from datetime import date

from core.bases.views import BaseTemplateView
from finance.models import TipoChoices
from finance.services.saldo_service import SaldoService


class PainelView(BaseTemplateView):
    template_name = 'dashboard/painel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano_atual = date.today().year
        service = SaldoService(self.request.user)

        saldo_data = service.calcular_saldo()
        total_receitas = saldo_data['total_receitas']
        total_despesas = saldo_data['total_despesas']
        saldo = saldo_data['saldo']
        percentual_economia = service.calcular_percentual_economia(total_receitas, total_despesas)

        resumo_mensal = service.resumo_mensal(ano_atual)
        resumo_despesas_cat = service.resumo_por_categoria(tipo=TipoChoices.DESPESA)
        resumo_receitas_cat = service.resumo_por_categoria(tipo=TipoChoices.RECEITA)
        ultimos_lancamentos = service.ultimos_lancamentos(limit=5)

        context.update({
            'saldo': saldo,
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'percentual_economia': percentual_economia,
            'ultimos_lancamentos': ultimos_lancamentos,
            'dados_grafico_mensal': resumo_mensal,
            'dados_grafico_despesas_cat': resumo_despesas_cat,
            'dados_grafico_receitas_cat': resumo_receitas_cat,
        })
        return context
