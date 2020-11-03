from django.db import models
from patient.models import Patient
from virus.models import Virus
from location.models import Location


class Case(models.Model):
    LOCAL_OR_IMPORTED = [
        ('Local', 'Local'),
        ('Imported', 'Imported')
    ]

    objects = models.Manager()
    case_number = models.CharField(max_length=20, primary_key=True) 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    virus = models.ForeignKey(Virus, on_delete=models.CASCADE)
    date_confirmed = models.DateField()
    local_or_imported = models.CharField(max_length=10, choices=LOCAL_OR_IMPORTED, default='Local')

    def __str__(self):
        return f"[{self.case_number}] {self.patient} ({self.virus})"


class CaseLocation(models.Model):
    CATEGORY = [
        ('Residence', 'Residence'),
        ('Workplace', 'Workplace'),
        ('Visit', 'Visit')
    ]
    
    objects = models.Manager()
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    category = models.CharField(max_length=10, choices=CATEGORY, default='Visit')

    def __str__(self):
        return f"[{self.case}] {self.location} ({self.date_from} - {self.date_to})"