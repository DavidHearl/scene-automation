from django.db import models


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
        ("Completed", "Completed"),
        ("Hold", "Hold"),
        ("Not Required", "Not Required")
    ]

    PRIORITY_CHOICES = (
        (0, 'Priority 0'),
        (1, 'Priority 1'),
        (2, 'Priority 2'),
        (3, 'Priority 3'),
    )

    AVAILABLE_MACHINES = [
        ("Machine 1", "Machine 1"),
        ("Machine 2", "Machine 2"),
        ("Machine 3", "Machine 3"),
        ("-", "-")
    ]

    default_value = "Queued"

    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=200)
    scans = models.IntegerField()
    point_cloud_size = models.BigIntegerField(default=0)
    raw_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    processed_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exported_size = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, blank=False)
    machine = models.CharField(max_length=20, choices=AVAILABLE_MACHINES, default="-")

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

