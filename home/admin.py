from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from home.models import Accidents


@admin.register(Accidents)
class SheetAdmin(ImportExportModelAdmin):
    pass



