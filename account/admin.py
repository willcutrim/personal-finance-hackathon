from django.contrib import admin

from account.models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'criado_em')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
