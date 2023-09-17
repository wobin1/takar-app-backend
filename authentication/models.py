from django.db import models


class TokenBlackList(models.Model):
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500)

    def __str__(self):
        return 'blackedListed'



