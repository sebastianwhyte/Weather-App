from configparser import ConfigParser
import argparse


''' Get the API key from the configuration file

	Expects a configuration file named "secrets,ini"
	'''
def get_api_key():
	config = ConfigParser()
	config.read("secrets.ini")

	return config["openweather"]["API_KEY"]		# access dictionary value to get the key


''' Handles the user interactions on the command line
	
	Returns: 
		argparse.Namespace: Populated namespace object

'''
def read_user_cli_args():
	parser = argparse.ArgumentParser(description = "Gets weather and temperature information for a city")

	return parser.parse_args()


if __name__ == "__main__":
	read_user_cli_args()
