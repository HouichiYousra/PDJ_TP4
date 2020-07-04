import django_tables2 as tables
from django_tables2.columns import checkboxcolumn
from Bill.models import *
from django.utils.html import format_html

import django_filters
class LigneFactureTable(tables.Table):
    action= '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit   = tables.TemplateColumn(action)
    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation','produit__id', 'produit__prix', 'qte' )

class ClientListTable(tables.Table):
    action= '<a href="{% url "client_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "client_delete" pk=record.id  %}" class="btn btn-danger">Supprimer</a>\
            <a href="{% url "client_factures_table" pk=record.id %}" class="btn btn-primary">Liste de factures</a>'
    edit   = tables.TemplateColumn(action)

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model=Utilisateur
        fields=('first_name','last_name','adresse','tel','sexe','chiffre')


class ClientFacturesListTable(tables.Table):
    action = '<a href="{% url "facture_update" pk=record.id client_pk=record.client.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "facture_delete" pk=record.id client_pk=record.client.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"


class FournisseurListTable(tables.Table):
    action= '<a href="{% url "fournisseur_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "fournisseur_delete" pk=record.id  %}" class="btn btn-danger">Supprimer</a>\
            <a href="{% url "fournisseur_produits_table" pk=record.id %}" class="btn btn-primary">Liste de produits</a>'
    edit   = tables.TemplateColumn(action)
    class Meta:
        model = Utilisateur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('first_name', 'last_name', 'adresse', 'tel', 'sexe', 'chiffre')


class ImageColumn(tables.Column):
     def render(self, value):
         return format_html('<img src="/produits/wikipedia.png" />', value)

class FournisseurProduitsListTable(tables.Table):
    action = '<a href="{% url "produit_update" pk=record.id fournisseur_pk=record.fournisseur.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "produit_delete" pk=record.id fournisseur_pk=record.fournisseur.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)
    imgelink = ImageColumn()
    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"

class ProduitsListTable(tables.Table):
    action = '<form action="" method="post">' \
             ' {% csrf_token %}' \
             '<btn type ="submit" href="#" class="btn btn-secondary"><span></span>Ajouter Pannier</btn>' \
             '</form>'
    edit = tables.TemplateColumn(action)
    imgelink = ImageColumn()
    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"

class FacturesListTable(tables.Table):
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"

class ClientChiffresTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model=Utilisateur
        fields=('first_name','last_name','adresse','tel','sexe','chiffre')

class FournisseurChiffresTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        model=Utilisateur
        fields = ('first_name', 'last_name', 'adresse', 'tel', 'sexe', 'chiffre')



class ProduitFilter(django_filters.FilterSet):
    class Meta:
        model = Produit
        fields = ['designation', 'prix', 'categorie', 'fournisseur']

