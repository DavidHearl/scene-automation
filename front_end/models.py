from django.db import models

# Time in minutes
hours_per_workday = 8
time_per_scan = 20
time_per_area = 60
minor_error_time = 15
major_error_time = 30
critical_error_time = 45
time_per_area_failed = 30

class Ship(models.Model):
    PRIORITY_CHOICES = (
        (0, 'Priority 0'),
        (1, 'Priority 1'),
        (2, 'Priority 2'),
        (3, 'Priority 3'),
    )

    name = models.CharField(max_length=200)
    contract_number = models.IntegerField(default=0, null=False, blank=False)
    company = models.CharField(max_length=200)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, blank=False)

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

            # Loop through the status choices and update weighting
            for i, status in enumerate(process_stage):
                if getattr(area, status) == "Completed" or getattr(area, status) == "Legacy" or getattr(area, status) == "No Data":
                    weighting += process_weighting[i]

            area_percentage = (100 * (weighting/1000) * (int(area.scans) / int(ship_total_scans)))  # Correct the formula

            percentage += area_percentage

        return round(percentage, 1)  # Round the percentage to one decimal place

    # Calculate the estimated completion date
    def estimated_completion(self):
        # Get number of scans and complete %
        total_scans = self.total_scans()
        completed_percentage = self.completed_percentage()

        # Multiply Total Scans x Time per Scan
        # Convert into hours and divide by working day
        estimated_time_per_scan = total_scans * time_per_scan / (60 * hours_per_workday)

        # Multipy number of areas x time per area
        total_areas = self.area_set.count()
        additional_time_per_area = total_areas * (time_per_area / (60 * hours_per_workday))

        # Calculate the additional time for failures
        total_failure_time = 0
        number_of_failures = 0
        for area in self.area_set.all():
          if area.registered == "Minor Fail":
                total_failure_time += int(area.scans) * minor_error_time
                number_of_failures += 1
          elif area.registered == "Major Fail":
                total_failure_time += int(area.scans) * major_error_time
                number_of_failures += 1
          elif area.registered == "Critical Fail":
                total_failure_time += int(area.scans) * critical_error_time
                number_of_failures += 1

        total_area_fail_time = (number_of_failures * time_per_area_failed) / (60 * hours_per_workday)
        total_failure_time = (total_failure_time / (60 * hours_per_workday)) + total_area_fail_time

        # Add additional time to total time
        estimated_time = estimated_time_per_scan + additional_time_per_area + total_failure_time

        # Ensure that the multiplication doesn't result in negative zero
        multiplier = 1 - (completed_percentage / 100)
        estimated_time *= 0 if multiplier == 0 else multiplier

        return round(estimated_time, 2)

    @classmethod
    def total_estimated_completion_for_all_ships(cls):
        # This line may result in a large number of database queries (one for each ship) 
        # and could be optimized by using the annotate method to calculate the estimated 
        # completion time directly in the database.
        total_estimated_time_for_all_ships = sum(ship.estimated_completion() for ship in cls.objects.all())
        return round(total_estimated_time_for_all_ships, 2)

    def __str__(self):
        return self.name


class Area(models.Model):
    STATUS_CHOICES = [
        ("No Data", "No Data"),
        ("Legacy", "Legacy"),
        ("Minor Fail", "Minor Fail"),
        ("Major Fail", "Major Fail"),
        ("Critical Fail", "Critical Fail"),
        ("Queued", "Queued"),
        ("WIP", "WIP"),
        ("Completed", "Completed")
    ]

    PRIORITY_CHOICES = (
        (0, 'Priority 0'),
        (1, 'Priority 1'),
        (2, 'Priority 2'),
        (3, 'Priority 3'),
    )

    default_value = "Completed"

    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=200)
    scans = models.IntegerField()
    point_cloud_size = models.BigIntegerField(default=0)
    raw_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    processed_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exported_size = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, blank=False)

    # Processing Operations
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

