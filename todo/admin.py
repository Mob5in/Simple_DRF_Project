from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Todo)
class TodoAdimn(admin.ModelAdmin):
    pass
