from django.contrib import admin

from .models import Year, Company, Project, Invoice, Fee

admin.site.register(Year)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Invoice)
admin.site.register(Fee)
