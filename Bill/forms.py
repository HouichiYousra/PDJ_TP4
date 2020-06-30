from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from Bill.models import Utilisateur


class ClientSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Utilisateur

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 1
        user.save()
        return user


class FournisseurSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Utilisateur

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = 2
        user.save()
        return user