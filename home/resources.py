from import_export import resources
from .models import Accident
from django.db import models
from import_export.fields import Field

class AccidentResource(resources.ModelResource):
    # id_accident = models.AutoField(db_column='ID_accident', primary_key=True)  # Field name made lowercase.
    # id_accident= Field(column_name='ID_accident')
    class Meta:
        model= Accident
        skip_unchanged = True
        report_skipped = True
        exclude = ('id_accident',)
        # skip_unchanged = True
        # report_skipped = True
        # exclude = ('ID_accident',)
        # skip_unchanged = True
        # report_skipped = False
        # import_id_fields = ('id_accident',)
        fields=('wilaya',	'date',	'CAUSE_ACC',	'TYPE_ROUTE',	'JOUR',
                          'MOIS',	'HEURE',	'Latitude',	'Longitude',	'NBRE_DEC',
                          'NBRE_BLESS',	'ANNEE_PERMIS',	'CAT_VEH',	'date_naiss_chau',
                          'AGE_CHAUFF',	'Temperature',	'VitesseVent',	'Precipitation',
                          'Humidite',	'Visibilite',	'CouvertureNuage',	'TempVent',
                          'Neige',	'Accident', )
def before_import_row(self, row, **kwargs):
    row['id_accident'] = None