from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    country = models.CharField(null=True, blank=True, max_length=256)
    city = models.CharField(null=True, blank=True, max_length=256)
    address = models.CharField(null=True, blank=True, max_length=256)
    allowed_subscriptions = models.PositiveIntegerField(default=3)
    # subscribed_to_home = models.BooleanField

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = "user_profiles"


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    country = models.CharField(null=True, blank=True, max_length=256)
    city = models.CharField(null=True, blank=True, max_length=256)
    subscription_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}, {self.country}, {self.city}"

    class Meta:
        db_table = "subscriptions"


class Weather(models.Model):
    country = models.CharField(max_length=128, null=False, blank=False)
    city = models.CharField(max_length=128, null=False, blank=False)
    temperature = models.CharField(max_length=128, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.country}, {self.city}"

    class Meta:
        db_table = "Weather"