from django.db import models
from datetime import datetime, date


class Job(models.Model):
    works_order_ref = models.CharField(max_length=100)
    operative_name = models.CharField(max_length=100)
    arrived_time = models.TimeField()
    departed_time = models.TimeField()
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def hours_on_site(self):
        arr = datetime.combine(date.today(), self.arrived_time)
        dep = datetime.combine(date.today(), self.departed_time)
        diff = dep - arr
        hours = diff.seconds / 3600
        return round(hours, 2)

    def labour_cost(self):
        rate = 28
        team_count = self.teammember_set.count()
        if team_count == 0:
            team_count = 1
        return round(self.hours_on_site() * rate * team_count, 2)

    def plant_cost(self):
        return round(sum(p.cost for p in self.plantitem_set.all()), 2)

    def total_cost(self):
        return round(self.labour_cost() + self.plant_cost(), 2)

    def __str__(self):
        return self.works_order_ref

    class Meta:
        ordering = ['-submitted_at']


class TeamMember(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlantItem(models.Model):
    PLANT_NAMES = [
        ('cherry_picker_full', 'Cherry picker (full day)'),
        ('cherry_picker_half', 'Cherry picker (half day)'),
        ('cable_drum', 'Cable drum'),
        ('road_saw', 'Road saw'),
        ('compactor', 'Compactor plate'),
        ('generator', 'Generator (day rate)'),
        ('traffic_mgmt', 'Traffic management kit'),
        ('sds_drill', 'SDS drill set'),
        ('pipe_freeze', 'Pipe freezing kit'),
        ('laser_level', 'Laser level kit'),
    ]

    COSTS = {
        'cherry_picker_full': 380,
        'cherry_picker_half': 210,
        'cable_drum': 90,
        'road_saw': 145,
        'compactor': 65,
        'generator': 120,
        'traffic_mgmt': 280,
        'sds_drill': 45,
        'pipe_freeze': 95,
        'laser_level': 55,
    }

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    item_key = models.CharField(max_length=50, choices=PLANT_NAMES)

    @property
    def cost(self):
        return self.COSTS.get(self.item_key, 0)

    @property
    def display_name(self):
        return dict(self.PLANT_NAMES).get(self.item_key, self.item_key)

    def __str__(self):
        return self.display_name


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('transit_van', 'Transit van'),
        ('tipper_35t', '3.5t tipper'),
        ('lorry_75t', '7.5t lorry'),
        ('cherry_truck', 'Cherry picker truck'),
        ('car_suv', 'Car / SUV'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    registration = models.CharField(max_length=20)
    arrived_time = models.TimeField()

    def __str__(self):
        return f"{self.registration} ({self.get_vehicle_type_display()})"
