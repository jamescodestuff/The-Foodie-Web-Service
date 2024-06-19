from flask import jsonify
import requests
import json


class GeocodioClient(object):
    """
    The client that makes request to the Geocodio
    to get the corresponding (latitude, longitude) pair.
    """

    def __init__(self, api_key):
        # key d993c933cb353b6b353361b669c55371d91db9b
        self.api_key = api_key

        self.url = "https://api.geocod.io/v1.7/geocode"
        pass

    def request(self, addr):
        params = {"q": addr, "api_key": self.api_key}
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                location = data["results"][0]["location"]
                return location["lat"], location["lng"]
            else:
                return "error: Address Is NULL"
        pass


class YelpClient(object):
    """
    The client that makes request to the Yelp
    to get a list of nearby restaurants.
    """

    def __init__(self, api_key):

        self.api_key = api_key
        self.url = "https://api.yelp.com/v3/businesses/search"
        pass

    def request(self, latitude, longitude):

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        params = {
            "latitude": latitude,
            "longitude": longitude,
        }
        if not latitude or not longitude:
            return "error: Address Is NULL"
        response = requests.get(self.url, headers=headers, params=params)
        data = response.json()
        if response.status_code == 200:
            format = []
            for business in data["businesses"]:
                formatted_restaurant = {
                    "name": business["name"],
                    "rating": str(business["rating"]),
                    "address": " ".join(business["location"]["display_address"]),
                }
                format.append(formatted_restaurant)
            return {"restaurants": format}
        else:
            print("ERROR")
        pass


GeocodioAPIKey = "d993c933cb353b6b353361b669c55371d91db9b"
yelpAPIKey = "IAY4A6iXW6s93OjOIlHg4ujBemCzrHijZzLAIeQeUnu73Kc4lPblhkukwUH8UAAP3S4oRapVMYdct8CYbPS-2zppd7fA-76EvWIbWinl_u0pFbDheZbDSxi-7RFAZXYx"

geo = GeocodioClient(GeocodioAPIKey)
yelp = YelpClient(yelpAPIKey)
