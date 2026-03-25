from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from finance.models import Categoria, Lancamento, TipoChoices
from finance.services.saldo_service import SaldoService


class SaldoServiceDateFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        cat = Categoria.objects.create(nome='Salário', tipo=TipoChoices.RECEITA, user=self.user)
        cat_desp = Categoria.objects.create(nome='Mercado', tipo=TipoChoices.DESPESA, user=self.user)
        Lancamento.objects.create(
            descricao='Salário Jan', valor=Decimal('5000'), tipo=TipoChoices.RECEITA,
            data=date(2026, 1, 15), categoria=cat, user=self.user,
        )
        Lancamento.objects.create(
            descricao='Mercado Jan', valor=Decimal('800'), tipo=TipoChoices.DESPESA,
            data=date(2026, 1, 20), categoria=cat_desp, user=self.user,
        )
        Lancamento.objects.create(
            descricao='Salário Fev', valor=Decimal('5000'), tipo=TipoChoices.RECEITA,
            data=date(2026, 2, 15), categoria=cat, user=self.user,
        )

    def test_saldo_sem_filtro(self):
        service = SaldoService(self.user)
        saldo = service.calcular_saldo()
        self.assertEqual(saldo['total_receitas'], Decimal('10000'))
        self.assertEqual(saldo['total_despesas'], Decimal('800'))

    def test_saldo_com_filtro_data_inicio(self):
        service = SaldoService(self.user, data_inicio=date(2026, 2, 1))
        saldo = service.calcular_saldo()
        self.assertEqual(saldo['total_receitas'], Decimal('5000'))
        self.assertEqual(saldo['total_despesas'], Decimal('0'))

    def test_saldo_com_filtro_data_fim(self):
        service = SaldoService(self.user, data_fim=date(2026, 1, 31))
        saldo = service.calcular_saldo()
        self.assertEqual(saldo['total_receitas'], Decimal('5000'))
        self.assertEqual(saldo['total_despesas'], Decimal('800'))

    def test_saldo_com_filtro_intervalo(self):
        service = SaldoService(self.user, data_inicio=date(2026, 1, 16), data_fim=date(2026, 2, 14))
        saldo = service.calcular_saldo()
        self.assertEqual(saldo['total_receitas'], Decimal('0'))
        self.assertEqual(saldo['total_despesas'], Decimal('800'))

    def test_ultimos_lancamentos_filtrados(self):
        service = SaldoService(self.user, data_inicio=date(2026, 2, 1))
        ultimos = list(service.ultimos_lancamentos())
        self.assertEqual(len(ultimos), 1)
        self.assertEqual(ultimos[0].descricao, 'Salário Fev')


class DashboardViewFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.login(username='test', password='pass')
        cat = Categoria.objects.create(nome='Renda', tipo=TipoChoices.RECEITA, user=self.user)
        Lancamento.objects.create(
            descricao='Salário', valor=Decimal('3000'), tipo=TipoChoices.RECEITA,
            data=date(2026, 3, 1), categoria=cat, user=self.user,
        )

    def test_dashboard_sem_filtro(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dashboard-filter-form')

    def test_dashboard_com_filtro_data(self):
        response = self.client.get('/?data_inicio=2026-03-01&data_fim=2026-03-31')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3000')

    def test_dashboard_filtro_exclui_fora_do_intervalo(self):
        response = self.client.get('/?data_inicio=2026-04-01')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '0,00')
