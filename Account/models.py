from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from localflavor.generic.models import IBANField


# Create your models here.
class BaseModel(models.Model):
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, related_name='updated_by', on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    iban = IBANField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('account-list')

    def __str__(self):
        return ' '.join([self.first_name, self.last_name, self.iban])
