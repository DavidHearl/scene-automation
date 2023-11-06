from django.db import models


class Ship(models.Model):
    name = models.CharField(max_length=200)
    contract_number = models.IntegerField(default=0, null=False, blank=False)
    company = models.CharField(max_length=200)

    def total_scans(self):
        return sum(area.scans for area in self.area_set.all())

    def completed_percentage(self):
        ship_total_scans = self.total_scans()

        if ship_total_scans == 0:
            return 0  # Avoid division by zero

        percentage = 0  # Initialize the percentage variable to 0

        for area in self.area_set.all():
            weighting = 0

            # Create a list of status choices
            process_stage = ["imported", "processed", "registered", "aligned", "cleaned", "point_cloud", "exported", "uploaded"]

            # Loop through the status choices and update weighting
            for status in process_stage:
                if getattr(area, status) == "Completed" or getattr(area, status) == "Legacy":
                    weighting += 1

            area_percentage = (100 * (weighting/8) * (int(area.scans) / int(ship_total_scans)))  # Correct the formula

            percentage += area_percentage

        return round(percentage, 1)  # Round the percentage to one decimal place

    def estimated_completion(self):
        total_scans = self.total_scans()
        completed_percentage = self.completed_percentage()

        estimated_time = total_scans * 15
        estimated_time = estimated_time / (60 * 8)
        estimated_time = estimated_time * -((completed_percentage / 100) - 1)
        
        return round(estimated_time, 2)

    def __str__(self):
        return self.name


class Area(models.Model):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=200)
    scans = models.IntegerField()

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

