from django.contrib import admin
from Bill.models import Utilisateur, Produit, Facture, LigneFacture, Categorie, LigneCommande, Commande

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Facture)
admin.site.register(Produit)
admin.site.register(LigneFacture)
admin.site.register(Categorie)
admin.site.register(LigneCommande)
admin.site.register(Commande)