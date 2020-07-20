# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NegativeSamples(models.Model):
    age_chauff = models.IntegerField(db_column='AGE_CHAUFF', blank=True, null=True)  # Field name made lowercase.
    annee_permis = models.DateField(db_column='ANNEE_PERMIS', blank=True, null=True)  # Field name made lowercase.
    cat_veh = models.CharField(db_column='CAT_VEH', max_length=30, blank=True, null=True)  # Field name made lowercase.
    couverturenuage = models.IntegerField(db_column='CouvertureNuage', blank=True, null=True)  # Field name made lowercase.
    heure = models.TimeField(db_column='HEURE', blank=True, null=True)  # Field name made lowercase.
    humidite = models.IntegerField(db_column='Humidite', blank=True, null=True)  # Field name made lowercase.
    jour = models.CharField(db_column='JOUR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    mois = models.CharField(db_column='MOIS', max_length=12, blank=True, null=True)  # Field name made lowercase.
    nbre_bless = models.IntegerField(db_column='NBRE_BLESS', blank=True, null=True)  # Field name made lowercase.
    nbre_dec = models.IntegerField(db_column='NBRE_DEC', blank=True, null=True)  # Field name made lowercase.
    neige = models.IntegerField(db_column='Neige', blank=True, null=True)  # Field name made lowercase.
    precipitation = models.IntegerField(db_column='Precipitation', blank=True, null=True)  # Field name made lowercase.
    type_route = models.CharField(db_column='TYPE_ROUTE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tempvent = models.IntegerField(db_column='TempVent', blank=True, null=True)  # Field name made lowercase.
    temperature = models.IntegerField(db_column='Temperature', blank=True, null=True)  # Field name made lowercase.
    visiblite = models.IntegerField(db_column='Visiblite', blank=True, null=True)  # Field name made lowercase.
    vitessevent = models.IntegerField(db_column='VitesseVent', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    date_naiss_chauff = models.DateField(blank=True, null=True)
    wilaya = models.CharField(max_length=20, blank=True, null=True)
    accidet = models.IntegerField(db_column='Accidet', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'negative_samples'


class Sheet1(models.Model):
    wilaya = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    cause_acc = models.CharField(db_column='CAUSE_ACC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type_route = models.CharField(db_column='TYPE_ROUTE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    jour = models.CharField(db_column='JOUR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    mois = models.CharField(db_column='MOIS', max_length=12, blank=True, null=True)  # Field name made lowercase.
    heure = models.TimeField(db_column='HEURE', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    nbre_dec = models.IntegerField(db_column='NBRE_DEC', blank=True, null=True)  # Field name made lowercase.
    nbre_bless = models.IntegerField(db_column='NBRE_BLESS', blank=True, null=True)  # Field name made lowercase.
    annee_permis = models.DateField(db_column='ANNEE_PERMIS', blank=True, null=True)  # Field name made lowercase.
    cat_veh = models.CharField(db_column='CAT_VEH', max_length=20, blank=True, null=True)  # Field name made lowercase.
    date_naiss_chauff = models.DateField(blank=True, null=True)
    age_chauff = models.IntegerField(db_column='AGE_CHAUFF', blank=True, null=True)  # Field name made lowercase.
    temperature = models.IntegerField(db_column='Temperature', blank=True, null=True)  # Field name made lowercase.
    vitessevent = models.IntegerField(db_column='VitesseVent', blank=True, null=True)  # Field name made lowercase.
    precipitation = models.IntegerField(db_column='Precipitation', blank=True, null=True)  # Field name made lowercase.
    humidite = models.IntegerField(db_column='Humidite', blank=True, null=True)  # Field name made lowercase.
    visibilite = models.IntegerField(db_column='Visibilite', blank=True, null=True)  # Field name made lowercase.
    couverturenuage = models.IntegerField(db_column='CouvertureNuage', blank=True, null=True)  # Field name made lowercase.
    tempvent = models.IntegerField(db_column='TempVent', blank=True, null=True)  # Field name made lowercase.
    neige = models.IntegerField(db_column='Neige', blank=True, null=True)  # Field name made lowercase.
    accident = models.IntegerField(db_column='Accident', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sheet1'
