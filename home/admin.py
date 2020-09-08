from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from home.models import Sheet1,Profile


@admin.register(Sheet1)
class SheetAdmin(ImportExportModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):
    pass
