from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from account.models import TimeStampModel


class Article(TimeStampModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("Title of Article", max_length=250, db_column="Title of the Article")
    description = models.TextField(blank=True, null=True, db_column="Description of Article")
    image = models.ImageField(upload_to='image', blank=True, null=True, verbose_name="Image path", db_column="Image")

    class Meta:
        db_table = "Articles"

    def __str__(self):
        return self.title