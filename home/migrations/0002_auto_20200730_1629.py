# Generated by Django 3.0.8 on 2020-07-30 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='accidents',
            fields=[
                ('wilaya', models.CharField(blank=True, max_length=20, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('cause_acc', models.CharField(blank=True, db_column='CAUSE_ACC', max_length=50, null=True)),
                ('type_route', models.CharField(blank=True, db_column='TYPE_ROUTE', max_length=50, null=True)),
                ('jour', models.CharField(blank=True, db_column='JOUR', max_length=12, null=True)),
                ('mois', models.CharField(blank=True, db_column='MOIS', max_length=12, null=True)),
                ('heure', models.TimeField(blank=True, db_column='HEURE', null=True)),
                ('latitude', models.FloatField(blank=True, db_column='Latitude', null=True)),
                ('longitude', models.FloatField(blank=True, db_column='Longitude', null=True)),
                ('nbre_dec', models.IntegerField(blank=True, db_column='NBRE_DEC', null=True)),
                ('nbre_bless', models.IntegerField(blank=True, db_column='NBRE_BLESS', null=True)),
                ('annee_permis', models.DateField(blank=True, db_column='ANNEE_PERMIS', null=True)),
                ('cat_veh', models.CharField(blank=True, db_column='CAT_VEH', max_length=20, null=True)),
                ('date_naiss_chauff', models.DateField(blank=True, null=True)),
                ('age_chauff', models.IntegerField(blank=True, db_column='AGE_CHAUFF', null=True)),
                ('temperature', models.IntegerField(blank=True, db_column='Temperature', null=True)),
                ('vitessevent', models.IntegerField(blank=True, db_column='VitesseVent', null=True)),
                ('precipitation', models.IntegerField(blank=True, db_column='Precipitation', null=True)),
                ('humidite', models.IntegerField(blank=True, db_column='Humidite', null=True)),
                ('visibilite', models.IntegerField(blank=True, db_column='Visibilite', null=True)),
                ('couverturenuage', models.IntegerField(blank=True, db_column='CouvertureNuage', null=True)),
                ('tempvent', models.IntegerField(blank=True, db_column='TempVent', null=True)),
                ('neige', models.IntegerField(blank=True, db_column='Neige', null=True)),
                ('accident', models.IntegerField(blank=True, db_column='Accident', null=True)),
                ('id_accident', models.AutoField(db_column='ID_accident', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'accidents',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Sheet1',
        ),
    ]
