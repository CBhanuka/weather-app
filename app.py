from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# OpenWeather API details
API_KEY = '80eb6174487b0c55f0d0e87a7fb7ea59'  # Replace with your actual API key
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# List of cities in Sri Lanka (expand this list as needed)
sri_lankan_cities = [
    # Colombo District (Major areas)
    "Colombo", "Dehiwala", "Mount Lavinia", "Moratuwa", "Kotte", "Kolonnawa",
    "Kaduwela", "Homagama", "Maharagama", "Kesbewa", "Boralesgamuwa", "Ratmalana",
    "Athurugiriya", "Avissawella", "Battaramulla", "Hanwella", "Hokandara",
    "Kadawatha", "Kohuwala", "Malabe", "Mulleriyawa", "Nugegoda", "Pannipitiya",
    "Piliyandala", "Rajagiriya", "Talawatugoda", "Wellampitiya",
    
    # Gampaha District (Major areas)
    "Gampaha", "Negombo", "Wattala", "Ja-Ela", "Kelaniya", "Ragama", "Minuwangoda",
    "Veyangoda", "Kiribathgoda", "Seeduwa", "Kandana", "Katunayake", "Peliyagoda",
    
    # Other major cities
    "Kandy", "Galle", "Jaffna", "Matara", "Anuradhapura", "Kurunegala", "Ratnapura",
    "Badulla", "Kalutara", "Polonnaruwa", "Hambantota", "Nuwara Eliya", "Trincomalee"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        print(f"City entered: {city}")  # Debug: print the city entered
        
        try:
            # Fetch weather data from OpenWeather API
            response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY, 'units': 'metric'})
            print(f"API Response URL: {response.url}")  # Debug: print the API request URL
            data = response.json()

            print(f"Weather data received: {data}")  # Debug: print the weather data
            
            if data['cod'] == 200:
                weather = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure']
                }
            else:
                error = f"City not found, please try again. API Response: {data.get('message', 'Unknown error')}"
        except requests.exceptions.RequestException as e:
            error = "Error fetching data from API. Please try again later."
    
    return render_template('index.html', weather=weather, error=error)


@app.route('/suggestions', methods=['GET'])
def suggestions():
    query = request.args.get('q')
    results = []

    # Filter cities in Sri Lanka based on the query
    for city in sri_lankan_cities:
        if query.lower() in city.lower():
            # Suggest city name with "LK" (country code for Sri Lanka)
            results.append({"name": f"{city}, LK", "country": "Sri Lanka", "lat": 0, "lon": 0})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
