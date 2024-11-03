from django.db import models
from base.models import PracticeModel, EducationalOrganizationModel, ActivityModel

class StudentApplicationModel(models.Model):
    STATUS = (
        ("Рассмотрение", "Рассмотрение"),
        ("Отклонено", "Отклонено"),
        ("Принято", "Принято"),
    )
    practice = models.ForeignKey(PracticeModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    educational_organization = models.ForeignKey(EducationalOrganizationModel, on_delete=models.SET_NULL, null=True)
    date_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=18)
    status = models.CharField(max_length=255, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class NotificationApplicationModel(models.Model):
    full_name = models.CharField(max_length=255)
    educational_organization = models.ForeignKey(EducationalOrganizationModel, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    activity = models.ForeignKey(ActivityModel, on_delete=models.SET_NULL, null=True) #Сделать ManyTomany
    
