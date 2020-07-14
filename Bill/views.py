from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.utils import TEMPLATE_PACK
from django.contrib.auth import login
from django.db import transaction
from django.db.models import Sum, F, ExpressionWrapper, fields, Count
from django.forms import formset_factory, ModelForm, inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_tables2 import SingleTableView, MultiTableMixin
from django.views import generic
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Field, Fieldset, HTML, ButtonHolder, LayoutObject
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
# Create your views here.
from Bill.chart import LineChart
from Bill.forms import ClientSignUpForm, FournisseurSignUpForm, PoduitSearchForm
from Bill.tables import *


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    total = facture.calculPrixTotal()
    context={}
    context['facture'] = facture
    context['prix'] = total
    return render(request, 'bill/facture_detail.html', context)

class FactureUpdate(SuccessMessageMixin,UpdateView):
    model = Facture
    fields = ['client', 'date']
    template_name = 'bill/CRUD/update.html'
    success_message = "La facture a été mise à jour avec succès"
    def get_form(self, form_class=None):
        messages.warning(self.request, "vous allez ajouter la facture")
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.fields['client']=forms.ModelChoiceField(queryset=Utilisateur.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_factures_table', kwargs={'pk':self.kwargs.get('client_pk')})
        return form

class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture
    
    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)
        
        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context

class FactureDelete(SuccessMessageMixin,DeleteView):
    model = Facture
    template_name = 'bill/CRUD/delete.html'
    success_message = "La facture a été suprime avec succès"
    def get_success_url(self):
        self.success_url = reverse('client_factures_table', kwargs={'pk':self.kwargs.get('client_pk')})
        return self.success_url

class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/CRUD/create.html'
    fields = ['facture', 'produit', 'qte']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form

class LigneFactureUpdateView(SuccessMessageMixin,UpdateView):
    model = LigneFacture
    template_name = 'bill/CRUD/update.html'
    fields = ['facture', 'produit', 'qte']
    success_message = "La facture a été mise à jour avec succès"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        messages.warning(self.request, "Attention, vous allez modifier la facture")
        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form

class LigneFactureDeleteView(SuccessMessageMixin,DeleteView):
    model = LigneFacture
    template_name = 'bill/CRUD/delete.html'
    success_message = "La facture a été supprimer avec succès"

    def get_success_url(self):
        messages.warning(self.request, "Attention, vous allez supprimer la facture")
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return self.success_url

class LignePanierUpdateView(SuccessMessageMixin,UpdateView):
    model = LignePanier
    template_name = 'bill/CRUD/update.html'
    fields = ['qte']
    success_message = "Le panier a été mise à jour avec succès"
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        messages.warning(self.request, "Attention, vous allez modifier le panier")
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('panier_table')
        return form

class LignePanierDeleteView(SuccessMessageMixin,DeleteView):
    model = LignePanier
    template_name = 'bill/CRUD/delete.html'
    success_message = "La ligne panier a été supprimer avec succès"

    def get_success_url(self):
        messages.warning(self.request, "Attention, vous allez supprimer la ligne panuer")
        self.success_url = reverse('panier_table')
        return self.success_url

class ClientListView(SingleTableView):
    template_name = 'bill/CRUD/list.html'
    model=Utilisateur

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        table = ClientListTable(Utilisateur.objects.filter(user_type=1).annotate(chiffre=Sum(F('factures__prix'))))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context

class ClientCreateView(CreateView):
    model = Utilisateur
    template_name = 'bill/CRUD/create.html'
    fields = ['first_name', 'last_name', 'adresse','tel','sexe']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form

class ClientUpdateView(UpdateView):
    model = Utilisateur
    template_name = 'bill/CRUD/update.html'
    fields = ('first_name', 'last_name', 'adresse', 'tel', 'sexe')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form

class ClientDeleteView(DeleteView):
    model = Utilisateur
    template_name = 'bill/CRUD/delete.html'
    success_url = reverse_lazy('clients_table')


class ClientFacturesListView(DetailView):
    template_name = 'bill/client_factures_table.html'
    model = Utilisateur

    def get_context_data(self, **kwargs):
        context = super(ClientFacturesListView, self).get_context_data(**kwargs)

        table = ClientFacturesListTable(Facture.objects.filter(client=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class LigneFactureForm(forms.ModelForm):

    class Meta:
        model = LigneFacture
        exclude = ()

LigneFactureFormSet = inlineformset_factory(
    Facture, LigneFacture, form=LigneFactureForm,
    fields=['produit', 'qte'], extra=1, can_delete=True
    )
class Formset(LayoutObject):
    template = "bill/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template


    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})

class FactureCreateView(CreateView):
    model = Facture
    template_name = 'bill/CRUD/create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client'] = forms.ModelChoiceField(
            queryset=Utilisateur.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.fields['date'] = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'))
        form.helper.layout = Layout(
            Div(
                Field('client'),
                Field('date'),
                Fieldset('Ajouter lignes',
                         Formset('lignes')),
            )
        )
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client_factures_table', kwargs={'pk': self.kwargs.get('client_pk')})
        return form

    def get_context_data(self, **kwargs):
        data = super(FactureCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['lignes'] = LigneFactureFormSet(self.request.POST)
        else:
            data['lignes'] = LigneFactureFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lignes = context['lignes']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if lignes.is_valid():
                lignes.instance = self.object
                lignes.save()
        return super(FactureCreateView, self).form_valid(form)

class FournisseurCreateView(CreateView):
    model = Utilisateur
    template_name = 'bill/CRUD/create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse_lazy('fournisseurs_table')
        return form

class FournisseurDeleteView(DeleteView):
    model = Utilisateur
    template_name = 'bill/CRUD/delete.html'
    success_url = reverse_lazy('fournisseurs_table')

class FournisseurUpdateView(UpdateView):
    model = Utilisateur
    fields = ('first_name', 'last_name', 'adresse', 'tel', 'sexe')
    template_name = 'bill/CRUD/update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseurs_table')
        return form

class FournisseurListView(SingleTableView):
    template_name = 'bill/CRUD/list.html'
    model= Utilisateur

    def get_context_data(self, **kwargs):
        context = super(FournisseurListView, self).get_context_data(**kwargs)

        table = FournisseurListTable(Utilisateur.objects.filter(user_type=2))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context

class ProduitListView(SingleTableView):
    template_name = 'bill/produit_table.html'
    model= Produit

    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)

        table = ProduitsListTable(Produit.objects.all())
        RequestConfig(self.request, paginate={"per_page": 4}).configure(table)
        context['table'] = table
        return context

class FacturesListView(SingleTableView):
    template_name = 'bill/CRUD/list.html'
    model= Facture

    def get_context_data(self, **kwargs):
        context = super(FacturesListView, self).get_context_data(**kwargs)

        table = ClientFacturesListTable(Facture.objects.all())
        RequestConfig(self.request, paginate={"per_page": 4}).configure(table)
        context['table'] = table
        return context

class CommandeListView(SingleTableView):
    template_name = 'bill/commande_table.html'
    model= Commande

    def get_context_data(self, **kwargs):
        context = super(CommandeListView, self).get_context_data(**kwargs)

        table = CommandeAdminListTable(Commande.objects.all())
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context

class CommandeClientListView(SingleTableView):
    template_name = 'bill/commande_table.html'
    model= Commande

    def get_context_data(self, **kwargs):
        context = super(CommandeClientListView, self).get_context_data(**kwargs)

        table = CommandeListTable(Commande.objects.all().filter(client=self.request.user))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context



class PanierListView(SingleTableView):
    template_name = 'bill/panier.html'
    model= LignePanier

    def get_context_data(self, **kwargs):
        context = super(PanierListView, self).get_context_data(**kwargs)

        table = PanierListTable(LignePanier.objects.all().filter(panier__client=self.request.user))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context

class FournisseurProduitsListView(DetailView):
    template_name = 'bill/fournisseur_produits_table.html'
    model = Utilisateur

    def get_context_data(self, **kwargs):
        context = super(FournisseurProduitsListView, self).get_context_data(**kwargs)

        table = FournisseurProduitsListTable(Produit.objects.filter(fournisseur=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class CommandeProduitsListView(DetailView):
    template_name = 'bill/fournisseur_produits_table.html'
    model = Commande

    def get_context_data(self, **kwargs):
        context = super(CommandeProduitsListView, self).get_context_data(**kwargs)

        table = CommandeProduitsListTable(Produit.objects.filter(lignes_com__commande=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        return context


class ProduitCreateView(CreateView):
    model = Produit
    template_name = 'bill/CRUD/create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['fournisseur'] = forms.ModelChoiceField(
            queryset=Utilisateur.objects.filter(id=self.kwargs.get('fournisseur_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_produits_table', kwargs={'pk': self.kwargs.get('fournisseur_pk')})
        return form

class ProduitUpdateView(UpdateView):
    model = Produit
    template_name = 'bill/CRUD/update.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_produits_table', kwargs={'pk':self.kwargs.get('fournisseur_pk')})
        return form

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'bill/CRUD/delete.html'
    def get_success_url(self):
        self.success_url = reverse('fournisseur_produits_table', kwargs={'pk':self.kwargs.get('fournisseur_pk')})
        return self.success_url

class DashboardTablesView(MultiTableMixin, TemplateView):

    template_name = "bill/dashboard.html"

    tables = [
        ClientChiffresTable(Utilisateur.objects.filter(user_type=1).annotate(chiffre=Sum(F('factures__prix'))).order_by('-chiffre')),
        FournisseurChiffresTable(Utilisateur.objects.filter(user_type=2).annotate(
            chiffre=Sum(ExpressionWrapper(F('produits__prix')*F('produits__lignes__qte'),output_field=fields.FloatField()))).order_by('-chiffre'))
    ]
    print(tables)
    table_pagination = {
        "per_page": 4
    }

class HomeView(TemplateView):
    template_name = 'bill/home.html'

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class ClientSignUpView(SuccessMessageMixin,CreateView):
    model = Utilisateur
    form_class = ClientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class FournisseurSignUpView(CreateView):
    model = Utilisateur
    form_class = FournisseurSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'fournisseur'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class ProduitSearchView(generic.CreateView):
    model = Produit
    form_class = PoduitSearchForm
    success_url = "/"


class FilteredProduitListView(SingleTableMixin, FilterView):
    table_class = ProduitsListTable
    model = Produit
    template_name = "bill/produit_filtre.html"

    filterset_class = ProduitFilter

def create_panier(request):
    if request.method == "POST":
        pks = request.POST.getlist("selection")
        selected_objects = Produit.objects.filter(pk__in=pks)
        utilisateur= Utilisateur.objects.get(pk= request.user.pk)
        if Panier.objects.filter(client=utilisateur).exists() == False:
            panier=Panier.objects.create(client=utilisateur)
            panier.save()
        else:
            panier= Panier.objects.get(client=utilisateur)
        print("count" + str(selected_objects.count()))
        for obj in selected_objects:
            if LignePanier.objects.filter(produit=obj, panier__client=utilisateur).exists():
                ligne= LignePanier.objects.get(produit=obj)
                ligne.qte =ligne.qte+1
                ligne.save()
            else:
                lign_panier= LignePanier.objects.create(panier=panier, produit=obj)
                lign_panier.save()
        return  redirect('panier_table')



def create_commande(request):
    if request.method == "POST":
        pks = request.POST.getlist("id")
        selected_objects = LignePanier.objects.filter(pk__in=pks)
        utilisateur= Utilisateur.objects.get(pk= request.user.pk)
        commande=Commande.objects.create(client=utilisateur)
        commande.save()
        print("count" + str(selected_objects.count()))
        for obj in selected_objects:
            lign_commande= LigneCommande.objects.create(commande=commande, produit=obj.produit, qte=obj.qte)
            lign_commande.save()
        LignePanier.objects.filter(pk__in=pks).delete()
        return  redirect('commande_client')

def valide_commande(request, pk):
    if request.method == "POST":
        pks = request.POST.get("id")
        print("iddd", str(pks))
        commande = Commande.objects.get(pk=pk)
        commande.valide= True
        commande.save()
        utilisateur = Utilisateur.objects.get(pk=request.user.pk)
        facture = Facture.objects.create(client=utilisateur)
        facture.save()
        lignes= LigneCommande.objects.filter(commande=commande)
        for l in lignes:
            facture_ligne= LigneFacture.objects.create(facture=facture, produit=l.produit, qte=l.qte)
            facture_ligne.calculPrix()
            facture_ligne.save()
        facture.calculPrixTotal()
        facture.save()
        return redirect('commande_table')