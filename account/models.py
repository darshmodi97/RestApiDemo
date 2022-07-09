from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", db_column="created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at", db_column="updated")

    class Meta:
        abstract = True


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")
        db_table = "Blacklisted Tokens"
