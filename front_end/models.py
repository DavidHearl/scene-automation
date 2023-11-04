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

    STATUS_CHOICES = [
        ("No Data", "No Data"),
        ("Legacy", "Legacy"),
        ("Failed", "Failed"),
        ("Queued", "Queued"),
        ("WIP", "WIP"),
        ("Completed", "Completed")
    ]

    imported = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    processed = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    registered = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    aligned = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    cleaned = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    point_cloud = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    exported = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")
    uploaded = models.CharField(max_length=20, choices=STATUS_CHOICES, default="No Data")

    def __str__(self):
        return self.area_name

