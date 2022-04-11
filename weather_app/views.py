from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Subscription, Weather

from django.http import HttpResponse

from .models import UserProfile


# note order of decorators
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    curr_user = request.user
    # if curr_user.is_anonymous
    # userprofile = UserProfile.objects.get(user=curr_user)
    data = {
        "first_name": curr_user.first_name,
        "last_name": curr_user.last_name
    }
    return Response(data)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscriptions(request):
    if request.method == 'POST':
        subscription = {
            'user': request.user,
            'country': request.data['country'],
            'city': request.data['city']
        }
        Subscription.objects.create(**subscription)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        subscriptions = Subscription.objects.filter(user=request.user)
        data = {'subs': [], 'allowed_subs': 0}
        for subscription in subscriptions:
            data['subs'].append({'id': subscription.id, 'country': subscription.country, 'city': subscription.city})
        user_profile = UserProfile.objects.get(user=request.user)
        data['allowed_subs'] = user_profile.allowed_subscriptions
        return Response(data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_details(request, id):
    sub = Subscription.objects.get(user=request.user, id=id)
    sub.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subscription_import(request):
    file_content = request.FILES['file'].file.read()
    file_as_str = file_content.decode()
    print(file_as_str)
    file_as_str = file_as_str.split("\r\n")
    print(file_as_str)
    for row in file_as_str:
        row = row.split(",")
        if row[0][0] == " ":
            row[0] = row[0][1:]
        if row[1][0] == " ":
            row[1] = row[1][1:]
        subscription = {
            'user': request.user,
            'country': row[0],
            'city': row[1]
        }
        Subscription.objects.create(**subscription)
        print(subscription)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['PUT', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "country": profile.country,
            "city": profile.city,
            "address": profile.address
        }
        return Response(data)
    elif request.method == 'PUT':
        user = request.user
        profile = UserProfile.objects.get(user=user)
        user.first_name = request.data['new_first_name']
        user.last_name = request.data['new_last_name']
        profile.country = request.data['new_country']
        profile.city = request.data['new_city']
        profile.address = request.data['new_address']
        user.save()
        profile.save()
        return Response(status=status.HTTP_200_OK)


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_weather(request):
#     url = "https://api.openweathermap.org/data/2.5/weather"
#     subs = []
#     for sub in request.data:
#         subs.append(sub)
#
#     weather_list =[]
#     for sub in subs:
#         weather = Weather.objects.filter(city=sub['city']).filter(country=sub['country'])
#
#
#     if city in manager.cache.keys() and datetime.datetime.now().timestamp() - manager.cache[city][
#         "TimeStamp"].timestamp() <= self.config.interval():
#         # print("time passed from the last update:")
#         # print(datetime.datetime.now().timestamp() - manager.cache[city]["TimeStamp"].timestamp())
#         # print("id for debugging:")
#         # print (id(manager.cache[city]["weather"]))
#         return manager.cache[city]["weather"]
#     else:
#         response = requests.get(
#             url,
#             params={"q": [city], "appid": "4b78ea80315fc7df43033eb466cae839", "units": "metric"}
#         )
#         manager.cache[city] = {"TimeStamp": datetime.datetime.now(), "weather": response.json()}
#         return response.json()



