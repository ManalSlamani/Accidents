from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from home.models import Accident


@admin.register(Accident)
class SheetAdmin(ImportExportModelAdmin):
    pass

