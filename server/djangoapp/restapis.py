import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Create a `get_request` to make HTTP GET requests

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
                                    id=dealer.get("id", None), lat=dealer.get("lat", None), long=dealer.get("long", None),
                                    short_name=dealer.get("short_name", ""),
                                    st=dealer.get("st", ""), zip=dealer.get("zip", ""), state=dealer.get("state", ""))
            results.append(dealer_obj)

    return results


def get_dealers_by_state(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
                                    id=dealer.get("id", None), lat=dealer.get("lat", None), long=dealer.get("long", None),
                                    short_name=dealer.get("short_name", ""),
                                    st=dealer.get("st", ""), zip=dealer.get("zip", ""), state=dealer.get("state", ""))
            results.append(dealer_obj)

    return results


def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        for dealer in dealers:
            if dealerId == dealer["id"]:
                dealer_obj = CarDealer(address=dealer.get("address", ""), city=dealer.get("city", ""), full_name=dealer.get("full_name", ""),
                                        id=dealer.get("id", None), lat=dealer.get("lat", None), long=dealer.get("long", None),
                                        short_name=dealer.get("short_name", ""),
                                        st=dealer.get("st", ""), zip=dealer.get("zip", ""), state=dealer.get("state", ""))
        results.append(dealer_obj)

    return results
    
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealer_reviews_from_cf(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["body"]["data"]
        # For each dealer object
        for review in reviews:
            review_obj = DealerReview(name=review.get("name", ""), dealership=review.get("dealership", None),
                                        review=review.get("review", ""), purchase=review.get("purchase", False),
                                        purchase_date=review.get("purchase_date", None), car_make=review.get("car_make", ""),
                                        car_model=review.get("car_model", None), car_year=review.get("car_year", None), sentiment="")
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results
    
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text, **kwargs):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/8f90c857-9d52-420c-9468-cf9290bb6785"
    api_key = "QhG7KyllLL1BW4NWzC8-DUg53xOo7OflGyq1so5xYUbs"
    
    authenticator = IAMAuthenticator(api_key) 
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(url) 
    response = natural_language_understanding.analyze(text=text, language="en", features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 
    label = response['sentiment']['document']['label'] 
    return label



