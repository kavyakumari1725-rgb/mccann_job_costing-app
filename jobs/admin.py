from django.contrib import admin
from .models import Job, TeamMember, PlantItem, Vehicle


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


class PlantItemInline(admin.TabularInline):
    model = PlantItem
    extra = 1


class VehicleInline(admin.TabularInline):
    model = Vehicle
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['works_order_ref', 'operative_name', 'arrived_time', 'departed_time', 'total_cost', 'submitted_at']
    inlines = [TeamMemberInline, PlantItemInline, VehicleInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'job']


@admin.register(PlantItem)
class PlantItemAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'job', 'cost']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration', 'vehicle_type', 'arrived_time', 'job']
