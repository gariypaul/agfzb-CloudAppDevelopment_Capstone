from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer,CarMake,CarModel
from .restapis import get_dealer_reviews_from_cf,get_request,get_dealers_from_cf,get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def signup(request):
    context = {}
    if request.method == "GET":
        return render (request, 'djangoapp/registration.html',context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html',context)



# Create a `contact` view to return a static contact page
def contact(request):
    context={}
    if request.method == "GET":
        return render(request,'djangoapp/contact.html',context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        login(request,user)

        return redirect("djangoapp:index")

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)

    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, password=password,first_name=first_name, last_name=last_name)

        login(request, user)

        return render(request, 'djangoapp/index.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://gariypaul-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {
            "dealerships":dealerships,
        }
        return render (request,"djangoapp/index.html",context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    url = ""
    if request.method == "GET":
        url = "https://gariypaul-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/dealership?id={dealer_id}"
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        context = {
            "reviews":reviews,
            "dealer_id":dealer_id
        }
        return render(request,'djangoapp/dealer_details.html',context)
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = f"https://5b93346d.us-south.apigw.appdomain.cloud/dealerships/dealer-get?dealerId={dealer_id}"
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)

