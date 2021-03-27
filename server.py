from flask import Flask, render_template, redirect, jsonify, request
import jinja2
import requests
import os

app = Flask(__name__)
app.secret_key = 'sendNoodsNow'
# app.jinja_env.undefined = StrictUndefined


foursquare_client_id = os.environ['CLIENT_ID']
foursquare_client_secret = os.environ['CLIENT_SECRET'] 
google_api_key = os.environ['GOOG_KEY']

#### NAVIGATION ####
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('home.html')
    
    elif request.method == 'POST':
        city = request.form.get('city') #grabbed user input and stored it in 'city' and 'query'
        query = request.form.get('query')

        url = "https://api.foursquare.com/v2/venues/search"
        payload = {'near': city,
                'query': query}
        
        r = requests.get(url, params=payload)

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

        return restaurantInfo
    
    else:
        return "No restaurants found"

        # data = {'query': query, 'city': city} #created a dictionary

        # return jsonify(data)
         
        #grab the data from POST form, input it into Foursquare API request
        # return first restaurant that fulfills that search



if __name__ == '__main__':
    # connect_to_db(app)
    app.run(debug=True, host="0.0.0.0") 