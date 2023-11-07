from django.contrib import admin
from import_export import resources
from .models import DemandData

class DemandDataResource(resources.ModelResource):
    class Meta:
        model = DemandData

