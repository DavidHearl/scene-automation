from django.db import models


class Ship(models.Model):
    name = models.CharField(max_length=200)
    contract_number = models.IntegerField()
    company = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Area(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=200)

    def __str__(self):
        return self.area_name


class Status(models.Model):
    area_name = models.ForeignKey(Area, on_delete=models.CASCADE)
    imported = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    registered = models.BooleanField(default=False)
    aligned = models.BooleanField(default=False)
    cleaned = models.BooleanField(default=False)
    point_cloud = models.BooleanField(default=False)
    exported = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.area_name.area_name} - {self.area_name.ship.name}"
