from django.contrib import admin

from location.models import Area, District, Division, Region, Union, Upazila


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    pass


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(Upazila)
class UpazilaAdmin(admin.ModelAdmin):
    pass


@admin.register(Union)
class UnionAdmin(admin.ModelAdmin):
    pass
