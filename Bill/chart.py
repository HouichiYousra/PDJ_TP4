from django.db.models import Sum, F, ExpressionWrapper, fields, Count
from jchart import Chart
from jchart.config import Axes, DataSet

from Bill.models import Facture, Categorie


class LineChart(Chart):
    chart_type = 'line'
    factures = Facture.objects.values('date').annotate(
        chiffre_affaire=Sum(
            ExpressionWrapper(F('lignes__produit__prix') * F('lignes__qte'), output_field=fields.FloatField())))

    def get_datasets(self, **kwargs):
        return [DataSet(
            color=(178, 26, 44),
            data=list(self.factures.values_list('chiffre_affaire', flat=True)),
            label="L'evolution du chiffre d'affaire"
        )

        ]

    def get_labels(self, *args, **kwargs):
        return list(self.factures.values_list('date', flat=True))

class RadarChart(Chart):
    chart_type = 'radar'
    categories = Categorie.objects.values('nom').annotate(chiffre_affaire=Sum(ExpressionWrapper(F('produits__prix')
                                                                                                * F(
        'produits__lignes__qte'), output_field=fields.FloatField())))

    def get_datasets(self, **kwargs):

        return [DataSet(
            color=(26,178,44),
            data=list(self.categories.values_list('chiffre_affaire', flat=True)),
            label="Chiffre d'affaire par categorie"
        )

        ]

    def get_labels(self, *args, **kwargs):
        return list(self.categories.values_list('nom', flat=True))

