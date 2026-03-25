from datetime import date

from core.bases.views import BaseTemplateView
from dashboard.forms import DashboardFilterForm
from finance.models import TipoChoices
from finance.services.saldo_service import SaldoService


class PainelView(BaseTemplateView):
    template_name = 'dashboard/painel.html'

    def get_filter_form(self):
        if not hasattr(self, '_filter_form'):
            self._filter_form = DashboardFilterForm(data=self.request.GET or None)
        return self._filter_form

    def get_date_filters(self):
        form = self.get_filter_form()
        data_inicio = None
        data_fim = None
        if form.is_valid():
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
        return data_inicio, data_fim

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano_atual = date.today().year
        data_inicio, data_fim = self.get_date_filters()
        service = SaldoService(self.request.user, data_inicio=data_inicio, data_fim=data_fim)

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
            'filter_form': self.get_filter_form(),
        })
        return context
