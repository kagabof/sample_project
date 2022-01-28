from django.db import models
from django.contrib.postgres.fields import ArrayField
from hashes_apps.utils.generators import ID_LENGTH, id_generater
from hashes_apps.apps.authentication.models import User


class Hash(models.Model):
    id = models.CharField(max_length=ID_LENGTH,
                          default=id_generater,
                          primary_key=True,
                          editable=False)
    added_timestamp = models.DateTimeField(auto_now_add=True)
    hash = ArrayField(models.FloatField(null=False), null=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hashes")

    class Meta:
        ordering = ['-added_timestamp']
