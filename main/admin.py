from django.contrib import admin

# Register your models here.
from .models import Account, Insight

admin.site.register(Account)
admin.site.register(Insight)