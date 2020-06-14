from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.utils import TEMPLATE_PACK
from django.db import transaction
from django.db.models import Sum, F, ExpressionWrapper, fields, Count
from django.forms import formset_factory, ModelForm, inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_tables2 import SingleTableView, MultiTableMixin

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Div, Field, Fieldset, HTML, ButtonHolder, LayoutObject
from django.urls import reverse_lazy


# Create your views here.
from Bill.chart import LineChart
from Bill.tables import *


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    total = facture.calculPrixTotal()
    context={}
    context['facture'] = facture
    context['prix'] = total
    return render(request, 'bill/facture_detail.html', context)

def client_detail_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    context={}
    context['client'] = client
    return render(request, 'bill/client_detail.html', context)

class FactureUpdate(UpdateView):
    model = Facture
    fields = ['client', 'date']
    template_name = 'bill/facture_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client']=forms.ModelChoiceField(queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
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
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context

class FactureDelete(DeleteView):
    model = Facture
    template_name = 'bill/facture_delete.html'
    def get_success_url(self):
        self.success_url = reverse('client_factures_table', kwargs={'pk':self.kwargs.get('client_pk')})

class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form

class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'bill/facture_update.html'
    fields = ['facture', 'produit', 'qte']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form

class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/ligne_delete.html'
    
    def get_success_url(self):
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})

class ClientListView(SingleTableView):
    template_name = 'bill/clients_table.html'
    model=Client

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        table = ClientListTable(Client.objects.all().annotate(chiffre=Sum(F('factures__prix'))))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context

class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/client_create.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form

class ClientUpdateView(UpdateView):
    model = Client
    template_name = 'bill/client_update.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('clients_table')
        return form

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/client_delete.html'
    success_url = reverse_lazy('clients_table')


class ClientFacturesListView(DetailView):
    template_name = 'bill/client_factures_table.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientFacturesListView, self).get_context_data(**kwargs)

        table = ClientFacturesListTable(Facture.objects.filter(client=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
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
    template_name = 'bill/facture_create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client'] = forms.ModelChoiceField(
            queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
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
    model = Fournisseur
    template_name = 'bill/fournisseur_create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse_lazy('fournisseurs_table')
        return form

class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/fournisseur_delete.html'
    success_url = reverse_lazy('fournisseurs_table')

class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    fields = '__all__'
    template_name = 'bill/fournisseur_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit', 'Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseurs_table')
        return form

class FournisseurListView(SingleTableView):
    template_name = 'bill/fournisseurs_table.html'
    model= Fournisseur
    table_class = FournisseurListTable

class FournisseurProduitsListView(DetailView):
    template_name = 'bill/fournisseur_produits_table.html'
    model = Fournisseur

    def get_context_data(self, **kwargs):
        context = super(FournisseurProduitsListView, self).get_context_data(**kwargs)

        table = FournisseurProduitsListTable(Produit.objects.filter(fournisseur=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


class ProduitCreateView(CreateView):
    model = Produit
    template_name = 'bill/produit_create.html'
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['fournisseur'] = forms.ModelChoiceField(
            queryset=Fournisseur.objects.filter(id=self.kwargs.get('fournisseur_pk')), initial=0)
        form.helper.add_input(Submit('submit', 'Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur_produits_table', kwargs={'pk': self.kwargs.get('fournisseur_pk')})
        return form

class ProduitUpdateView(UpdateView):
    model = Produit
    template_name = 'bill/produit_update.html'
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
    template_name = 'bill/Produit_delete.html'
    def get_success_url(self):
        self.success_url = reverse('fournisseur_produits_table', kwargs={'pk':self.kwargs.get('fournisseur_pk')})


class DashboardTablesView(MultiTableMixin, TemplateView):

    template_name = "bill/dashboard.html"

    tables = [
        ClientChiffresTable(Client.objects.all().annotate(chiffre=Sum(F('factures__prix'))).order_by('-chiffre')),
        FournisseurChiffresTable(Fournisseur.objects.all().annotate(
            chiffre=Sum(ExpressionWrapper(F('produits__prix')*F('produits__lignes__qte'),output_field=fields.FloatField()))).order_by('-chiffre'))
    ]

    table_pagination = {
        "per_page": 5
    }

