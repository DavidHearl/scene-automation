from django.db import models

# Time in minutes
time_per_scan = 20
time_per_area = 60

class Ship(models.Model):
    name = models.CharField(max_length=200)
    contract_number = models.IntegerField(default=0, null=False, blank=False)
    company = models.CharField(max_length=200)

    # Count the number of scans in each ship
    def total_scans(self):
        return sum(area.scans for area in self.area_set.all())

    # Calculate the completed percentage
    def completed_percentage(self):
        ship_total_scans = self.total_scans()

        if ship_total_scans == 0:
            return 0  # Avoid division by zero

        percentage = 0  # Initialize the percentage variable to 0

        for area in self.area_set.all():
            weighting = 0

            # Create a list of status choices
            process_stage = ["imported", "processed", "registered", "aligned", "cleaned", "point_cloud", "exported", "uploaded"]
            process_weighting = [12.5, 100, 100, 12.5, 75, 100, 500, 100]
            i = 0

            # Loop through the status choices and update weighting
            for status in process_stage:
                if getattr(area, status) == "Completed" or getattr(area, status) == "Legacy":
                    weighting += process_weighting[i]
                i += 1

            area_percentage = (100 * (weighting/1000) * (int(area.scans) / int(ship_total_scans)))  # Correct the formula

            percentage += area_percentage

        return round(percentage, 1)  # Round the percentage to one decimal place

    # Calculate the estimated completion date
    def estimated_completion(self):
        total_scans = self.total_scans()
        completed_percentage = self.completed_percentage()

        estimated_time_per_scan = total_scans * time_per_scan / (60 * 8)

        # Calculate the additional time based on the number of areas
        total_areas = self.area_set.count()
        additional_time_per_area = total_areas * (time_per_area / (60 * 8))

        estimated_time = estimated_time_per_scan + additional_time_per_area

        # Ensure that the multiplication doesn't result in negative zero
        multiplier = -((completed_percentage / 100) - 1)
        estimated_time *= 0 if multiplier == 0 else multiplier

        return round(estimated_time, 2)

    @classmethod
    def total_estimated_completion_for_all_ships(cls):
        total_estimated_time_for_all_ships = sum(ship.estimated_completion() for ship in cls.objects.all())
        return round(total_estimated_time_for_all_ships, 2)

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

    default_value = "Completed"

    imported = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    processed = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    registered = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    aligned = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    cleaned = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    point_cloud = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    exported = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
    uploaded = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)

    def __str__(self):
        return self.area_name

