from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    body = models.TextField()
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class EducationalOrganizationModel(models.Model):
    TYPE_OF_EDUCATIONAL_ORGANIZATION = (
        ("ВУЗ", "ВУЗ"),
        ("Колледж", "Колледж"),
    )
    name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_OF_EDUCATIONAL_ORGANIZATION, blank=True)

    def __str__(self):
        return self.name

class SubdivisionModel(models.Model):
    DEPARTMENT = (
        ('ГСП', 'Газтройпром'),
        ('ГСП 2', 'ГСП2'),
    )
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=255, choices=DEPARTMENT, blank=True)
    def __str__(self):
        return self.name
    
class ActivityModel(models.Model):
    TYPE_OF_ACTIVTY = (
        ('Нефтегазовая', 'Нефтегазовая'),
        ('Офисная', 'Офисная'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_OF_ACTIVTY, blank=True)
    def __str__(self):
        return self.name

class PracticeModel(models.Model):
    name = models.CharField(max_length=255)
    subdivision = models.ForeignKey(SubdivisionModel, on_delete=models.SET_NULL, null=True)
    activity = models.ManyToManyField(ActivityModel)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


