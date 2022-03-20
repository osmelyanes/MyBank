from django.contrib import admin

# Register your models here.
from Account.models import Person

admin.site.register(Person)
