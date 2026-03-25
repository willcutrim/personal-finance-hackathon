from django.contrib.auth.models import User

from core.bases.repositories import BaseRepository


class UserRepository(BaseRepository):
    model = User

    @classmethod
    def get_by_username(cls, username):
        return User.objects.filter(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.objects.filter(email=email).first()

    @classmethod
    def create_user(cls, username, email, password):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

    @classmethod
    def update_profile(cls, user, **data):
        for field, value in data.items():
            setattr(user, field, value)
        user.save(update_fields=list(data.keys()))
        return user

    @classmethod
    def change_password(cls, user, new_password):
        user.set_password(new_password)
        user.save(update_fields=['password'])
        return user
