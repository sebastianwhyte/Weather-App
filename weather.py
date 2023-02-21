from configparser import ConfigParser
import argparse


''' Get the API key from the configuration file

	Expects a configuration file named "secrets,ini"
	'''
def _get_api_key():
	config = ConfigParser()
	config.read("secrets.ini")

	return config["openweather"]["API_KEY"]		# access dictionary value to get the key


''' Handles the user interactions on the command line
	
	Returns: 
		argparse.Namespace: Populated namespace object

'''
def read_user_cli_args():
	parser = argparse.ArgumentParser(description = "Gets weather and temperature information for a city")

	# Define city argument to take more than one word and define its help text
	parser.add_argument("city", nargs = "+", type = str, help = "Enter the city name")

	# Define boolean for imperial units and define its help text
	parser.add_argument("--i", "--imperial", action = "store_true", help = "Display the temperature in imperial units",)

	return parser.parse_args()


if __name__ == "__main__":
	user_args = read_user_cli_args()
	print(user_args.city, user_args.imperial)

