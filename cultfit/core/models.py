from django.db import models

# Create your models here.

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField()
    Instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField(default=0)
    registered_clients = models.JSONField(default=list, blank=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'registered_clients'):
            self.registered_clients = []