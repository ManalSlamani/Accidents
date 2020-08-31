from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from home.models import Sheet1


@admin.register(Sheet1)
class SheetAdmin(ImportExportModelAdmin):
    pass



