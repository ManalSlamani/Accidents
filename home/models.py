from django.db import models
from django.contrib.auth.models import User



class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class NegativeSamples(models.Model):
    age_chauff = models.IntegerField(db_column='AGE_CHAUFF', blank=True, null=True)  # Field name made lowercase.
    annee_permis = models.DateField(db_column='ANNEE_PERMIS', blank=True, null=True)  # Field name made lowercase.
    accident = models.IntegerField(db_column='Accident', blank=True, null=True)  # Field name made lowercase.
    cat_veh = models.CharField(db_column='CAT_VEH', max_length=50, blank=True, null=True)  # Field name made lowercase.
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
    cause_acc = models.CharField(db_column='CAUSE_ACC', max_length=80, blank=True,
                                 null=True)  # Field name made lowercase.
    type_route = models.CharField(db_column='TYPE_ROUTE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tempvent = models.IntegerField(db_column='TempVent', blank=True, null=True)  # Field name made lowercase.
    temperature = models.IntegerField(db_column='Temperature', blank=True, null=True)  # Field name made lowercase.
    visibilite = models.IntegerField(db_column='visibilite', blank=True, null=True)  # Field name made lowercase.
    vitessevent = models.IntegerField(db_column='VitesseVent', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)
    date_naiss_chauff = models.DateField(blank=True, null=True)
    wilaya = models.CharField(max_length=20, blank=True, null=True)
    accident = models.IntegerField(db_column='Accident', blank=True, null=True)  # Field name made lowercase.
    id_acc = models.AutoField(primary_key=True, default= 0)

    class Meta:
        managed = True
        db_table = 'negative_samples'

class Accident(models.Model):
    wilaya = models.CharField(max_length=80, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    cause_acc = models.CharField(db_column='CAUSE_ACC', max_length=80, blank=True, null=True)  # Field name made lowercase.
    type_route = models.CharField(db_column='TYPE_ROUTE', max_length=80, blank=True, null=True)  # Field name made lowercase.
    jour = models.CharField(db_column='JOUR', max_length=12, blank=True, null=True)  # Field name made lowercase.
    mois = models.CharField(db_column='MOIS', max_length=12, blank=True, null=True)  # Field name made lowercase.
    heure = models.TimeField(db_column='HEURE', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    nbre_dec = models.IntegerField(db_column='NBRE_DEC', blank=True, null=True)  # Field name made lowercase.
    nbre_bless = models.IntegerField(db_column='NBRE_BLESS', blank=True, null=True)  # Field name made lowercase.
    annee_permis = models.DateTimeField(db_column='ANNEE_PERMIS', blank=True, null=True)  # Field name made lowercase.
    cat_veh = models.CharField(db_column='CAT_VEH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_naiss_chauff = models.DateTimeField(blank=True, null=True)
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
    id_accident = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'Accident'
