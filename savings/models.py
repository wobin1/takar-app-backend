from django.db import models
from django.db import models
from user.models import CustomUser
from django.utils.timezone import now
import uuid


class Savings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    savings_owner = models.ForeignKey(CustomUser, related_name="saving_owners", on_delete=models.CASCADE)
    savings_name = models.CharField(max_length=200)
    savings_goal = models.IntegerField(default=0000)
    creation_date = models.DateTimeField(default=now)
    deadline = models.DateTimeField(default=now)
    amount_saved = models.IntegerField(default=0000) 
    reciepient = models.ForeignKey(CustomUser, related_name="savings_reciepients", on_delete=models.CASCADE)

    def __str__(self):
        return self.savings_name