from django.contrib import admin
from django.urls import re_path, path
from Bill import views
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table_detail'),
    re_path(r'^facture_table_create/(?P<facture_pk>\d+)/$', views.LigneFactureCreateView.as_view(), name='facture_table_create'),
    re_path(r'^lignefacture_delete/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureDeleteView.as_view(), name='lignefacture_delete'),
    re_path(r'^lignefacture_update/(?P<pk>\d+)/(?P<facture_pk>\d+)/$', views.LigneFactureUpdateView.as_view(), name='lignefacture_update'),
    re_path(r'^facture_update/(?P<pk>\d+)/$', views.FactureUpdate.as_view(), name='facture_detail'),

    re_path(r'^client_detail/(?P<pk>\d+)/$', views.client_detail_view, name='client_detail'),
    re_path(r'^clients_table/', views.ClientListView.as_view(), name='clients_table'),
    re_path(r'^client_create/', views.ClientCreateView.as_view(), name='client_create'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(),
            name='client_delete'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(),
            name='client_update'),
    re_path(r'^client/(?P<pk>\d+)/factures_table/', views.ClientFacturesListView.as_view(), name='client_factures_table'),
    re_path(r'^client/(?P<client_pk>\d+)/facture_create/', views.FactureCreateView.as_view(), name='facture_create'),
    path('admin/', admin.site.urls),
    re_path(r'^fournisseurs_table/', views.FournisseurListView.as_view(), name='fournisseurs_table'),
    re_path(r'^fournisseur_create/', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(),
            name='fournisseur_delete'),
    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(),
            name='fournisseur_update'),
]