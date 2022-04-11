from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    # path("subscriptions/", views.subscriptions),
    # path("user_settings/current", views.current_user_settings),

    path("users/current", views.current_user),
    path("users/current/subscriptions/", views.subscriptions),
    path("users/current/subscriptions/<int:id>", views.subscription_details),
    path("users/current/userprofile/", views.user_profile),
    path("users/current/subscriptions/import/", views.subscription_import),
    path('token/', obtain_auth_token),
    # adding DELETE to token
]
