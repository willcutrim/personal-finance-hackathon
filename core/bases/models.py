from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def ativos(self):
        return self.filter(deletado_em__isnull=True)

    def deletados(self):
        return self.filter(deletado_em__isnull=False)

    def delete(self):
        return super().update(deletado_em=timezone.now())

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deletado_em=None)


class ActiveManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().ativos()


class AllObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    pass


class BaseModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    deletado_em = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = ActiveManager()
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True

    @property
    def esta_deletado(self):
        return self.deletado_em is not None

    def delete(self, using=None, keep_parents=False):
        self.deletado_em = timezone.now()
        self.save(update_fields=["deletado_em", "atualizado_em"])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.deletado_em = None
        self.save(update_fields=["deletado_em", "atualizado_em"])
