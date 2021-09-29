from django.contrib import admin

from agent.models import Agent, Distributor, DSO, MA


@admin.register(MA)
class MAAdmin(admin.ModelAdmin):
    pass


@admin.register(Distributor)
class DistributorAdmin(admin.ModelAdmin):
    pass


@admin.register(DSO)
class DSOAdmin(admin.ModelAdmin):
    pass


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    pass

