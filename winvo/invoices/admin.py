from django.contrib import admin

from .models import Company, Project, Invoice, Fee, Config

admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Invoice)
admin.site.register(Fee)
admin.site.register(Config)
