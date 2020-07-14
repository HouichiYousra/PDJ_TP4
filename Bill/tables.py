import django_tables2 as tables
from django_tables2.columns import checkboxcolumn
from Bill.models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_tables2.utils import Accessor, AttributeDict
import django_filters

from django.utils.html import escape
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
    edit= tables.TemplateColumn(action)
    class Meta:
        model = Utilisateur
        template_name = "django_tables2/bootstrap4.html"
        fields = ('first_name', 'last_name', 'adresse', 'tel', 'sexe', 'chiffre')

class ImageColumn(tables.Column):
    def render(self, value):
         return format_html('<img src="/media/img/{}.jpg" />', value)

class FournisseurProduitsListTable(tables.Table):
    action = '<a href="{% url "produit_update" pk=record.id fournisseur_pk=record.fournisseur.id %}" class="btn btn-warning">Modifier</a>\
            <a href="{% url "produit_delete" pk=record.id fournisseur_pk=record.fournisseur.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)

    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"


class CommandeProduitsListTable(tables.Table):
    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"

class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name




class ImageColumnp(tables.Column):
     def render(self, value):
        return mark_safe('<img src="D:/Bill-TP3/DB/PDJ_TP4/%s" />'
                         % escape(value))
class ProduitsListTable(tables.Table):
    # action = '<a href="{% url "add_panier" produit_id=record.id %}" class="btn btn-warning">Ajouter</a>'
    # Ajouter = tables.TemplateColumn(action)
    selection = CheckBoxColumnWithName(verbose_name="selection", accessor="pk")

    imgelink = ImageColumnp(verbose_name="IMAGE", accessor="image")
    def get_product(self):
        product=[]
        for row in self.rows:
            if row.select.is_checked():
                product.append(row.pk)
        return product

    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"


class PanierListTable(tables.Table):
    action = '<a href="{% url "lignepanier_update" pk=record.id panier_pk=record.panier.id %}" class="btn btn-warning">Modifier</a>\
                <a href="{% url "lignepanier_delete" pk=record.id panier_pk=record.panier.id %}" class="btn btn-danger">Supprimer</a>'
    edit = tables.TemplateColumn(action)
    class Meta:
        model = LignePanier
        template_name = "django_tables2/bootstrap4.html"

class CommandeListTable(tables.Table):
    action = '<a href="{% url "commande_produits_table" pk=record.id %}" class="btn btn-primary">Ligne Commande</a>'
    detail = tables.TemplateColumn(action)
    class Meta:
        model = Commande
        template_name = "django_tables2/bootstrap4.html"

class CommandeAdminListTable(tables.Table):
    action = '<form action="{% url "commande_valide" pk=record.id %}" method="post">{% csrf_token %}<input type="submit" class="btn btn-primary"/> </form>' \
             '<a href="{% url "commande_produits_table" pk=record.id %}" class="btn btn-primary">Ligne Commande</a>'
    detail = tables.TemplateColumn(action)
    class Meta:
        model = Commande
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

