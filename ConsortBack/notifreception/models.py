from django.db import models

class Notification(models.Model):
    received_date = models.DateField()
    received_time = models.TimeField()
    issuing_entity = models.CharField(max_length=255)
    case_number = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    receptionist = models.CharField(max_length=255)
    internal_delivery_time = models.TimeField()
    internal_collaborator = models.CharField(max_length=255)
    final_delivery_datetime = models.DateTimeField()

    def __str__(self):
        return f"Notification for {self.case_number} - {self.recipient}"
