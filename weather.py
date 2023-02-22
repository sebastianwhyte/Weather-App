from configparser import ConfigParser
from urllib import parse, error, request
from pprint import pp
import argparse
import json
import sys
import style


# All api calls will share the same endpoint
BASE_WEATHER_API_URL =	"http://api.openweathermap.org/data/2.5/weather"

THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


''' 
Get the API key from the configuration file

Expects a configuration file named "secrets,ini"

'''

def _get_api_key():
	config = ConfigParser()
	config.read("secrets.ini")

	return config["openweather"]["API_KEY"]		# access dictionary value to get the key


''' 
Handles the user interactions on the command line
	
Returns: argparse.Namespace: Populated namespace object

'''

def read_user_cli_args():
	parser = argparse.ArgumentParser(description = "Gets weather and temperature information for a city")

	# Define city argument to take more than one word and define its help text
	parser.add_argument("city", nargs = "+", type = str, help = "Enter the city name")

	# Define boolean for imperial units and define its help text
	parser.add_argument("-i", "--imperial", action = "store_true", help = "Display the temperature in imperial units",)

	return parser.parse_args()


'''
Builds the query we use for the API call

Arguments: city_input 		city specified by the user
		   imperial  		boolean indicating whether or not to use imperial units

Returns: string of URL formatted for call to OpenWeather's city name endpointß

'''

def build_weather_query(city_input, imperial = False):
	API_KEY = _get_api_key()

	# Join the words that make up a city name with a whitespace character if city name is more than one word
	city_name = " ".join(city_input)

	# Encode string to URL encoded format
	url_encoded_city_name = parse.quote_plus(city_name)

	# Check if imperial is true
	units = "imperial" if imperial else "metric"

	url = (f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"f"&units={units}&appid={API_KEY}")

	return url


'''
Makes an API request to the given url and returns the retreived data as a Python object 

Arguments: query_url 	string of formatted url for OpenWeather's city name endpoint

Returns: dict 			weather info for the specified city

'''

def get_weather_data(query_url):

	# Makes http request and saves its response
	#response = request.urlopen(query_url)

	try: 
		response = request.urlopen(query_url)

	except error.HTTPError as http_error:
		if http_error.code == 401:
			sys.exit("Authorization Failed. Check your API Key.")
		elif http_error.code == 404:
			sys.exit("No weather data found for this city")
		else:
			sys.exit(f"Error ({http_error.code})")


	# Read the retrieved data
	data = response.read()


	try:
		# Converts json string to a dict 
		return json.loads(data)
	except:
		sys.exit("Failed to read server response")


'''
Prints the formmated weather info about a city

Arguments: weather_data (dict)		API response from OpenWeather by city name
		   imperial					boolean that indicates whether we will use imperial units
	
'''

def display_weather_info(weather_data, imperial = False):
	city = weather_data["name"]
	weather = weather_data["weather"][0]["description"]
	weather_id = weather_data["weather"][0]["id"]
	temperature = weather_data["main"]["temp"]
	feels_like = weather_data["main"]["feels_like"]

	style.change_color(style.INVERT)
	print(f"{city: ^{style.PADDING}}", end = "")
	style.change_color(style.CLEAR)
	
	weather_icon, color = select_weather_display(weather_id)

	style.change_color(color)

	print(f"\t{weather_icon} ", end = " ")
	print(f"{weather.capitalize(): ^{style.PADDING}}", end = " ")

	style.change_color(style.CLEAR)

	print(f"({temperature}°{'F' if imperial else 'C'})")

	print(f"Feels like ({feels_like}°{'F' if imperial else 'C'}:{style.PADDING})")




def select_weather_display(weather_id):
	
	if weather_id in THUNDERSTORM:
		display = ("🌩️", style.RED)
	elif weather_id in DRIZZLE:
		display = ("💧", style.CYAN)
	elif weather_id in RAIN:
		display = ("💦", style.BLUE)
	elif weather_id in SNOW:
		display = ("❄️", style.WHITE)
	elif weather_id in ATMOSPHERE:
		display = ("🌀", style.BLUE)
	elif weather_id in CLEAR:
		display = ("☀️", style.YELLOW)
	elif weather_id in CLOUDY:
		display = ("☁️", style.WHITE)
	else:
		display = ("🌈", style.CLEAR)	

	return display


if __name__ == "__main__":
	user_args = read_user_cli_args()
	#print(user_args.city, user_args.imperial, "\n")

	query_url = build_weather_query(user_args.city, user_args.imperial);
	#print(query_url)

	weather_data = get_weather_data(query_url)

	display_weather_info(weather_data, user_args.imperial)

