from flask import Flask, render_template, redirect, jsonify, request
import jinja2
import requests
import os
import module 
import json

app = Flask(__name__)
app.secret_key = 'sendNoodsNow'
# app.jinja_env.undefined = StrictUndefined

# foursquare_client_id = os.environ['CLIENT_ID']
# foursquare_client_secret = os.environ.get['CLIENT_SECRET'] 
# google_api_key = os.environ.get['GOOG_KEY']

#### NAVIGATION ####
@app.route('/')
def index():
    return render_template('index.html')


def geocode_map():
    """geocode map and grab lat/long"""

    street_add = request.form.get("address")
    address = " ".join([street_add, "Alameda, CA"]) 

    url= "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {"address": address, "key": module.get_api_key("GOOG_KEY")}
    req = requests.get(url, params=payload)
    res = req.json()
    print(res)
    result = res['results'][0]
    
    lat_lng = []
    lat = result["geometry"]["location"]["lat"]
    lng = result["geometry"]["location"]["lng"]
    lat_lng.append(lat)
    lat_lng.append(lng)
    lat_long = str(lat_lng)
    
    return lat_long


@app.route('/home')
def homepage():
    return render_template('home.html')

    
@app.route('/home', methods = ['POST'])
def homepage_query():
    city = request.form.get('city') #grabbed user input and stored it in 'city' and 'query'
    query = request.form.get('query')
    
    latlng = geocode_map()
    foursq_id = module.get_4sq_id('CLIENT_ID')
    foursq_secret = module.get_4sq_secret('CLIENT_SECRET')

    url = "https://api.foursquare.com/v2/venues/search"
    payload = {'near': city, 'll': latlng, 'query': query, 'client_id': foursq_id, 'client_secret': foursq_secret}
    r = requests.get(url, params=payload)

    print("-------------------------------------------")
    print("this API call worked")

    result = json.loads(r.request(url, 'GET')[1])

    if result['response']['venues']:
        restaurant = result['response']['venues'][0]
        venue_id = restaurant['id']
        restaurant_name = restaurant['name']
        restaurant_address = restaurant['location']['formattedAddress']

        """format address into one string"""
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address 
    
    restaurantInfo = {'name': restaurant_name, 'address': restaurant_address}

    return render_template("results.html", name=restaurant_name, address=restaurant_address)
    
    # else:
    #     return "No restaurants found"


if __name__ == '__main__':
    # connect_to_db(app)
    app.run(debug=True, host="0.0.0.0") 
