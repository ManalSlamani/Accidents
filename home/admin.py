from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from home.models import Accident


@admin.register(Accident)
class SheetAdmin(ImportExportModelAdmin):
    pass
class AccidentsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'wilaya', 'date')
    search_fields = ('wilaya', 'date')
    list_filter = ('wilaya',)

