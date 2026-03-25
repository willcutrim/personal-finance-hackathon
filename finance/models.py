from django.contrib.auth.models import User
from django.db import models

from core.bases.models import BaseModel


class TipoChoices(models.TextChoices):
    RECEITA = 'RECEITA', 'Receita'
    DESPESA = 'DESPESA', 'Despesa'


class Categoria(BaseModel):
    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField('Tipo', max_length=10, choices=TipoChoices.choices)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categorias',
        verbose_name='Usuário',
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
        unique_together = [['nome', 'tipo', 'user']]
        indexes = [
            models.Index(fields=['tipo'], name='categoria_tipo_idx'),
            models.Index(fields=['user'], name='categoria_user_idx'),
        ]

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Lancamento(BaseModel):
    descricao = models.CharField('Descrição', max_length=200)
    valor = models.DecimalField('Valor', max_digits=12, decimal_places=2)
    tipo = models.CharField('Tipo', max_length=10, choices=TipoChoices.choices)
    data = models.DateField('Data')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='lancamentos',
        verbose_name='Categoria',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lancamentos',
        verbose_name='Usuário',
    )

    class Meta:
        verbose_name = 'Lançamento'
        verbose_name_plural = 'Lançamentos'
        ordering = ['-data', '-id']
        indexes = [
            models.Index(fields=['data'], name='lancamento_data_idx'),
            models.Index(fields=['tipo'], name='lancamento_tipo_idx'),
            models.Index(fields=['categoria'], name='lancamento_categoria_idx'),
            models.Index(fields=['user'], name='lancamento_user_idx'),
        ]

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'
