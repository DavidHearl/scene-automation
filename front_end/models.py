from django.db import models
from django.contrib.auth.models import User


class Statistics(models.Model):
	total_time = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	total_scans = models.IntegerField(default=0)
	total_stars = models.IntegerField(default=0)
	total_raw_storage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	total_processed_storage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	total_exported_storage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	
	average_scans_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	average_scans_per_area = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	average_areas_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	average_completion_time_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)

	average_raw_storage_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	average_processed_storage_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	average_exported_storage_per_ship = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class Ship(models.Model):
	PRIORITY_CHOICES = (
		(0, 'Priority 0'),
		(1, 'Priority 1'),
		(2, 'Priority 2'),
		(3, 'Priority 3'),
		(4, 'Priority 4'),
	)

	name = models.CharField(max_length=200)
	contract_number = models.IntegerField(default=0, null=False, blank=False)
	company = models.CharField(max_length=200)
	priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, blank=False)
	image = models.ImageField(null=True, blank=True)
	time_remaining = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)

	stars = models.IntegerField(default=0)
	completed_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	total_scans = models.IntegerField(default=0)

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

	default_value = "Queued"

	ship = models.ForeignKey(Ship, on_delete=models.CASCADE)

	area_name = models.CharField(max_length=200)
	scans = models.IntegerField()
	point_cloud_size = models.BigIntegerField(default=0)
	raw_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	processed_size = models.DecimalField(max_digits=5, decimal_places=2, default=0)
	exported_size = models.DecimalField(max_digits=5, decimal_places=2,default=0)
	priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, blank=False)
	time_remaining = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)

	calcualted_priority = models.DecimalField(max_digits=10, decimal_places=8, default=0, null=True, blank=True)
	star = models.BooleanField(default=False)

	# Processing Operations
	processed = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
	registered = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
	cleaned = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
	point_cloud = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
	exported = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)
	uploaded = models.CharField(max_length=20, choices=STATUS_CHOICES, default=default_value)

	def __str__(self):
		return self.area_name


class Machine(models.Model):
	name = models.CharField(max_length=200)
	currently_processing = models.OneToOneField(Ship, on_delete=models.CASCADE, null=True, blank=True)

	status = models.BooleanField(default=False)
	processing_capacity = models.DecimalField(max_digits=3, decimal_places=2)

	# CPU Specifications
	cpu = models.CharField(max_length=50)
	cpu_core_count = models.IntegerField()
	cpu_thread_count = models.IntegerField()
	cpu_base_frequency = models.DecimalField(max_digits=5, decimal_places=2)
	cpu_turbo_frequency = models.DecimalField(max_digits=5, decimal_places=2)
	cpu_cache = models.IntegerField()
	cpu_tdp = models.IntegerField()
	
	# CPU Benchmarks
	cpu_interger_math = models.IntegerField()
	cpu_floating_point_math = models.IntegerField()
	cpu_data_encryption = models.IntegerField()
	cpu_data_compression = models.IntegerField()
	cpu_single_thread = models.IntegerField()

	# Memory Specifications
	ram_capacity = models.IntegerField()
	ram_type = models.CharField(max_length=50)
	ram_frequency = models.IntegerField()

	# Storage Specifications
	storage_capacity = models.IntegerField()
	storage_read_speed = models.IntegerField()
	storage_write_speed = models.IntegerField()

	# GPU Specifications
	gpu = models.CharField(max_length=50)
	gpu_memory = models.IntegerField()
	gpu_pixel_rate = models.DecimalField(max_digits=10, decimal_places=2)
	gpu_texture_rate = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name


class Booking(models.Model):
	SCANNER = [
		("red", "red"),
		("blue", "blue"),
		("both", "both"),
	]

	start_date = models.DateField(null=True)
	end_date = models.DateField(null=True)
	scanner = models.CharField(max_length=10, choices=SCANNER)

	def clean(self):
		super().clean()
		if self.end_date < self.start_date:
			raise ValidationError("End date cannot be earlier than start date.")


# -----------------------------------------------------------------
# ---------------------------- Logging ----------------------------
# -----------------------------------------------------------------

class PageVisit(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	page = models.CharField(max_length=200)
	timestamp = models.DateTimeField(auto_now_add=True)
	time_remaining = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
