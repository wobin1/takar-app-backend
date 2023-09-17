from django.db import models
from user.models import CustomUser
from django.utils.timezone import now
import uuid


class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_date = models.DateTimeField(default=now)
    transaction_type = models.CharField(max_length=255)
    transaction_amount = models.FloatField()
    transaction_description = models.TextField(null=True)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_type
