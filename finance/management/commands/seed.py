from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from account.models import Perfil
from finance.models import Categoria, Lancamento, TipoChoices


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais para o usuário willyam'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='willyam',
            defaults={
                'first_name': 'Willyam',
                'email': 'willyam@email.com',
            },
        )
        if created:
            user.set_password('1234will')
            user.save()
            self.stdout.write(self.style.SUCCESS('Usuário willyam criado.'))
        else:
            self.stdout.write('Usuário willyam já existe.')

        Perfil.objects.get_or_create(user=user)

        cat_salario, _ = Categoria.objects.get_or_create(
            nome='Salário', tipo=TipoChoices.RECEITA, user=user,
        )
        cat_alimentacao, _ = Categoria.objects.get_or_create(
            nome='Alimentação', tipo=TipoChoices.DESPESA, user=user,
        )
        cat_transporte, _ = Categoria.objects.get_or_create(
            nome='Transporte', tipo=TipoChoices.DESPESA, user=user,
        )
        self.stdout.write(self.style.SUCCESS('3 categorias criadas/verificadas.'))

        lancamentos = [
            {
                'descricao': 'Salário Março',
                'valor': Decimal('8500.00'),
                'tipo': TipoChoices.RECEITA,
                'data': date(2026, 3, 5),
                'categoria': cat_salario,
            },
            {
                'descricao': 'Supermercado',
                'valor': Decimal('620.50'),
                'tipo': TipoChoices.DESPESA,
                'data': date(2026, 3, 10),
                'categoria': cat_alimentacao,
            },
            {
                'descricao': 'Uber mensal',
                'valor': Decimal('185.00'),
                'tipo': TipoChoices.DESPESA,
                'data': date(2026, 3, 15),
                'categoria': cat_transporte,
            },
        ]

        for item in lancamentos:
            Lancamento.objects.get_or_create(
                descricao=item['descricao'],
                user=user,
                defaults=item,
            )
        self.stdout.write(self.style.SUCCESS('3 lançamentos criados/verificados.'))
        self.stdout.write(self.style.SUCCESS('Seed concluído!'))
