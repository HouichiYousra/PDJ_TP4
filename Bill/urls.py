from django.contrib import admin
from django.urls import re_path, path
from Bill import views
from Bill.chart import LineChart, RadarChart

urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(extra_context={'type':'facture'}), name='facture_table_detail'),
    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(extra_context={'type':'facture'}), name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(extra_context={'type':'ligne facture'}), name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(extra_context={'type':'ligne facture'}), name='lignefacture_update'),
    re_path(r'^facture_update/(?P<pk>\d+)/(?P<client_pk>\d+)/$', views.FactureDetailView.as_view(extra_context={'type':'facture'}), name='facture_update'),
    re_path(r'^facture_delete/(?P<pk>\d+)/(?P<client_pk>\d+)/$', views.FactureDelete.as_view(extra_context={'type':'facture'}), name='facture_delete'),

    re_path(r'^client_detail/(?P<pk>\d+)/$', views.client_detail_view, name='client_detail'),
    re_path(r'^clients_table/', views.ClientListView.as_view(extra_context={'type':'client'}), name='clients_table'),
    re_path(r'^client_create/', views.ClientCreateView.as_view(extra_context={'type':'client'}), name='client_create'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(extra_context={'type':'client'}),
            name='client_delete'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(extra_context={'type':'client'}),
            name='client_update'),
    re_path(r'^client/(?P<pk>\d+)/factures_table/', views.ClientFacturesListView.as_view(extra_context={'type':'facture'}), name='client_factures_table'),
    re_path(r'^client/(?P<client_pk>\d+)/facture_create/', views.FactureCreateView.as_view(extra_context={'type':'facture'}), name='facture_create'),

    path('admin/', admin.site.urls),

    re_path(r'^fournisseurs_table/', views.FournisseurListView.as_view(extra_context={'type':'fournisseur'}), name='fournisseurs_table'),
    re_path(r'^fournisseur_create/', views.FournisseurCreateView.as_view(extra_context={'type':'fournisseur'}), name='fournisseur_create'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(extra_context={'type':'fournisseur'}),
            name='fournisseur_delete'),
    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(extra_context={'type':'fournisseur'}),
            name='fournisseur_update'),
    re_path(r'^fournisseur/(?P<pk>\d+)/produits_table/', views.FournisseurProduitsListView.as_view(extra_context={'type':'fournisseur'}), name='fournisseur_produits_table'),
    re_path(r'^fournisseur/(?P<fournisseur_pk>\d+)/produit_create/', views.ProduitCreateView.as_view(extra_context={'type':'fournisseur'}), name='produit_create'),
    re_path(r'^produit_update/(?P<pk>\d+)/(?P<fournisseur_pk>\d+)/$', views.ProduitUpdateView.as_view(extra_context={'type':'produit'}), name='produit_update'),
    re_path(r'^produit_delete/(?P<pk>\d+)/(?P<fournisseur_pk>\d+)/$', views.ProduitDeleteView.as_view(extra_context={'type':'produit'}), name='produit_delete'),
    re_path(r'^dashboard/', views.DashboardTablesView.as_view(extra_context={'line_chart': LineChart(), 'radar_chart': RadarChart()}),name='dashboard'),

]