from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_request, post_request
from .restapis import get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def my_view(request):
    return render(request, 'static_template.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')



# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp') 
        else:
            # Handle invalid login credentials
            return render(request, 'djangoapp/index.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'djangoapp/index.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('/djangoapp')


# Create a `registration_request` view to handle sign up request
def signup_request(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Redirect to a success page or login page
        return redirect('/djangoapp')
    else:
        return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ae1641c-2e45-4777-8638-cee7629cdbee/dealership-package/get-dealership/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships if dealer.short_name is not None])
        # Return a list of dealer short names
        return HttpResponse(dealer_names)

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ae1641c-2e45-4777-8638-cee7629cdbee/dealership-package/get-dealership/api/dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ae1641c-2e45-4777-8638-cee7629cdbee/default/get_all_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ae1641c-2e45-4777-8638-cee7629cdbee/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=dealer_id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]           
            payload["car_model"] = car.name
            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ae1641c-2e45-4777-8638-cee7629cdbee/default/post_review"

            post_request(review_post_url, new_payload, id=dealer_id)
        return redirect("djangoapp:dealer_details", id=dealer_id)

