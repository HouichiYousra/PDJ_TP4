from django.db.models import Sum, F, ExpressionWrapper, fields, Count
from jchart import Chart
from jchart.config import Axes

from Bill.models import Fournisseur, Categorie


class LineChart(Chart):
    chart_type = 'line'

    def get_datasets(self, **kwargs):
        fournisseurs=Fournisseur.objects.all().annotate(
            chiffre=Sum(ExpressionWrapper(F('produits__prix')*F('produits__lignes__qte'),output_field=fields.FloatField())))

        return [{
            'label': "Evolution du chiffre d'affaire par fournisseur",
            'data': [{'x': fournisseur.nom, 'y': fournisseur.chiffre} for fournisseur in fournisseurs]
        }]


class RadarChart(Chart):
    chart_type = 'radar'

    def get_datasets(self, **kwargs):
        categories=Categorie.objects.values('nom').annotate(chiffre_affaire=Sum(ExpressionWrapper(F('produits__prix')
                                                      *F('produits__lignes__qte'),output_field=fields.FloatField())))
        print(categories[0]['nom'])
        return [{
            'label': "chiffre d'affaire par catégorie",
            'data': {
                'label': [categorie['nom'] for categorie in categories],
                'datasets': [{
                    'data': [categorie['chiffre_affaire'] for categorie in categories],
            } ]
        }
        }]


