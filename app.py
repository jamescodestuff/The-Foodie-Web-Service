from flask import Flask, jsonify
from flask import request

import argparse
import requests
import json

from clients import GeocodioClient, YelpClient

app = Flask(__name__)
GeocodioAPIKey = "d993c933cb353b6b353361b669c55371d91db9b"
yelpAPIKey = "IAY4A6iXW6s93OjOIlHg4ujBemCzrHijZzLAIeQeUnu73Kc4lPblhkukwUH8UAAP3S4oRapVMYdct8CYbPS-2zppd7fA-76EvWIbWinl_u0pFbDheZbDSxi-7RFAZXYx"

geo = GeocodioClient(GeocodioAPIKey)
yelp = YelpClient(yelpAPIKey)


@app.route("/restaurant/<restaurant_addr>", methods=["GET"])
def restaurant(restaurant_addr):
    if request.method == "GET":
        lat, long = geo.request(restaurant_addr)
        if not lat or not long:
            return jsonify({"error": "Address Is NULL Or API Might Be Down"}),400
        
        data = yelp.request(lat, long)
        if not data:
                return jsonify({"error": "Yelp API Might Be Down"}), 503
        
        return jsonify(data), 200
    
    else:
        return jsonify({"error": "Bad Request"}), 405
        pass



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000, help="port number.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app.run(port=args.port)
