from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django_select2 import forms as s2forms
from django import forms
from Bill.models import Utilisateur, Produit


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


class DesignationWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "designation",
    ]

class PrixWidget(s2forms.ModelSelect2Widget):
    search_fields = [
            "prix__icontains",
        ]

class FournisseurWidget(s2forms.ModelSelect2Widget):
    search_fields = [
            "username__icontains",
        ]

class CategorieWidget(s2forms.ModelSelect2Widget):
    search_fields = [
            "categorie__icontains",
        ]


class PoduitSearchForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = "__all__"
        widgets = {
            "designation": DesignationWidget,
            "prix": PrixWidget,
            "fournisseur" : FournisseurWidget,
            "categorie": CategorieWidget,
        }
