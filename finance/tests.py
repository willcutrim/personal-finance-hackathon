from django.contrib.auth.models import User
from django.test import TestCase

from finance.models import Categoria, TipoChoices


class CategoriaFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.client.login(username='test', password='pass')
        Categoria.objects.create(nome='Alimentação', tipo=TipoChoices.DESPESA, user=self.user)
        Categoria.objects.create(nome='Transporte', tipo=TipoChoices.DESPESA, user=self.user)
        Categoria.objects.create(nome='Salário', tipo=TipoChoices.RECEITA, user=self.user)

    def test_lista_sem_filtro(self):
        response = self.client.get('/finance/categorias/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alimentação')
        self.assertContains(response, 'Transporte')
        self.assertContains(response, 'Salário')

    def test_filtro_por_nome(self):
        response = self.client.get('/finance/categorias/?nome=alim')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alimentação')
        self.assertNotContains(response, 'Transporte')
        self.assertNotContains(response, 'Salário')

    def test_filtro_nome_vazio_retorna_todos(self):
        response = self.client.get('/finance/categorias/?nome=')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alimentação')
        self.assertContains(response, 'Transporte')

    def test_filtro_sem_resultado(self):
        response = self.client.get('/finance/categorias/?nome=xyz')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Alimentação')
        self.assertNotContains(response, 'Transporte')

    def test_filtro_nao_mostra_categorias_outro_usuario(self):
        other = User.objects.create_user(username='other', password='pass')
        Categoria.objects.create(nome='Alimentação', tipo=TipoChoices.DESPESA, user=other)
        response = self.client.get('/finance/categorias/?nome=alim')
        self.assertEqual(response.status_code, 200)
        # Deve mostrar apenas 1 resultado (do user logado)
        self.assertContains(response, 'Alimentação', count=1)
