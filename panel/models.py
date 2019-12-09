from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from accounting.models import ConsumerSite


class ConsumerSiteAllowedField(models.Model):
    site = models.ForeignKey(ConsumerSite, related_query_name='CustomerSiteAllowedFields',
                             related_name='CustomerSiteAllowedFields',
                             on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('site', 'field_name')

