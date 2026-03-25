from django.urls import path

from dashboard.views import PainelView

app_name = 'dashboard'

urlpatterns = [
    path('', PainelView.as_view(), name='painel'),
]
