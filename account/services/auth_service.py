from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import transaction

from account.models import Perfil
from account.repositories.user_repository import UserRepository
from core.bases.services import BaseService


class AuthService(BaseService):
    repository_class = UserRepository

    def register(self, username, email, password):
        if UserRepository.get_by_username(username):
            raise ValidationError('Este nome de usuário já está em uso.')
        if UserRepository.get_by_email(email):
            raise ValidationError('Este e-mail já está cadastrado.')

        with transaction.atomic():
            user = UserRepository.create_user(username=username, email=email, password=password)
            Perfil.objects.create(user=user)

        return user

    def authenticate_user(self, username, password):
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            raise ValidationError('Usuário ou senha inválidos.')
        return user

    def login_user(self, user):
        login(self.request, user)

    def logout_user(self):
        logout(self.request)
