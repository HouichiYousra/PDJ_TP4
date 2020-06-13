from django.db import models
from django import utils

from django.urls import reverse

# Create your models here.

class Client(models.Model):
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length = 10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices = SEXE)

    def __str__(self):
        return self.nom + ' ' + self.prenom

class Fournisseur(models.Model):
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, default=None, blank=True, null=True,related_name='produits')

    def __str__(self):
        return self.designation
    
    
class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='factures')
    date = models.DateField(default=utils.timezone.now)
    prix = models.IntegerField(default=0,editable=False)
    def get_absolute_url(self):
        return reverse('facture_detail', kwargs={'pk': self.id})
    def __str__(self):
        return str(self.client)+' : '+ str(self.date)

    def calculPrixTotal(self):
        lignes = list(LigneFacture.objects.filter(facture=self))
        total = 0
        if (len(lignes)!= 0):
            for ligne in lignes:
                total += LigneFacture.calculPrix(ligne)
        return total

    def save(self, *args, **kwargs):
        self.prix = self.calculPrixTotal()
        super(Facture, self).save(*args, **kwargs)


class LigneFacture(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,related_name='lignes')
    qte = models.IntegerField(default=1)
    prix=models.IntegerField(default=0,editable=False)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produit', 'facture'], name="produit-facture")
        ]

    def calculPrix(self):
        return self.qte * self.produit.prix

    def save(self, *args, **kwargs):
        self.prix = self.calculPrix()
        super(LigneFacture, self).save(*args, **kwargs)
        self.facture.calculPrixTotal()
        self.facture.save()