from django.db import models
from user.models import CustomUser
from django.utils.timezone import now
import uuid



class Alawi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_owner = models.ForeignKey(CustomUser, related_name="owner", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    payment_sequence = models.CharField(max_length=200)
    amount_to_be_paid = models.IntegerField(default=0000)
    payment_date = models.DateField(default=now)
    creation_date = models.DateTimeField(default=now)
    initial_deposite = models.IntegerField(default=0000)
    product_balance = models.IntegerField(default=0000) 
    reciepient = models.ForeignKey(CustomUser, related_name="reciepients", on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
