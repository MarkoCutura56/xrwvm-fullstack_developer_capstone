from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse # noqa
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect # noqa
from django.contrib.auth import logout
from django.contrib import messages # noqa
from datetime import datetime # noqa
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


logger = logging.getLogger(__name__)
@csrf_exempt # noqa
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)
@csrf_exempt # noqa
def registration(request):
    context = {} # noqa
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False # noqa
    try:
        User.objects.get(username=username)
        username_exist = True
    except:# noqa
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password,
                                        email=email)
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


# @csrf_exempt # noqa
def get_dealerships(request, state="All"):
    if (state == "All"):
        endpoint = '/fetchDealers/'
    else:
        endpoint = '/fetchDealers/'+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if (dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if (dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})# noqa
    return JsonResponse({"CarModels": cars})


def add_review(request):
    if (request.user.is_anonymous == False): # noqa
        data = json.loads(request.body)
        try:
            response = post_review(data)# noqa
            return JsonResponse({"status": 200})
        except:# noqa
            return JsonResponse({"status": 401,"message": "Error in posting review"})# noqa
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
