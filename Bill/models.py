from django.contrib.auth.models import AbstractUser
from django.db import models
from django import utils
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from .sendEmail import send

# Create your models here.
class Categorie(models.Model):
    nom=models.CharField(max_length=50)

class Utilisateur(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'client'),
        (2, 'fournisseur'),
    )
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,null=True,blank=True)
    adresse = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=10, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE)

    def __str__(self):
        return self.username

    @property
    def is_client(self):
        return self.user_type==1

    @property
    def is_fournisseur(self):
        return self.user_type == 2




class Produit(models.Model):
    designation = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    image=models.ImageField(upload_to='produits/',null=True,blank=True)
    fournisseur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, default=None, blank=True, null=True,related_name='produits')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                    related_name='produits')

    def __str__(self):
        return self.designation
    
    
class Facture(models.Model):
    client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,related_name='factures')
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


class Commande(models.Model):
    client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commandes')
    date = models.DateField(default=utils.timezone.now)
    valide=models.BooleanField(default=False)


class LigneCommande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,related_name='lignes_com')
    qte = models.IntegerField(default=1)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes_com')




@receiver(post_save, sender=Facture)
def define_permission(sender, **kwargs):
    send("confirmer votre commande", "confirmation facture", ["gh_ishakboushaki@esi.dz"])
