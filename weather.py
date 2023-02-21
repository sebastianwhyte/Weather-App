from configparser import ConfigParser
from urllib import parse
import argparse
import json

# All api calls will share the same base url / endpoint
BASE_WEATHER_API_URL =	"http://api.openweathermap.org/data/2.5/weather"


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


if __name__ == "__main__":
	user_args = read_user_cli_args()
	print(user_args.city, user_args.imperial, "\n")
	query_url = build_weather_query(user_args.city, user_args.imperial);
	print(query_url)

