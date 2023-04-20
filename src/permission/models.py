import datetime
import uuid

from django.db import models


# Create your models here.
class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100)
    granted_date = models.DateField(blank=True, null=True, default=datetime.date.today)
    name = models.CharField(
        max_length=100,
        blank=True,
    )
    description = models.TextField(blank=True)
