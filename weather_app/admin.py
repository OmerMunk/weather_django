from django.contrib import admin
from .models import Subscription, UserProfile

# Register your models here.
admin.site.register(Subscription)
admin.site.register(UserProfile)