from django.db import models

# Create your models here.
class Event(models.Model):
    subject = models.CharField(max_length=100)
    event = models.CharField(max_length =100)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.subject} - {self.event} - {self.due_date}"
