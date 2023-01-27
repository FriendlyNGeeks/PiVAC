import json

def fetch_Settings():
	#stored in project directory
	default_config = 'default_config.json'
	#set UNC path after auto mount is established
	remote_config = '/usr/local/share/remote_config.json'
	#set for if statement
	fetchConfig = "null"

	try:
		with open(remote_config, 'r') as remote_config:
			print("Remote Config found")
			fetchConfig = json.load(remote_config)
	except IOError as e:
		if e.errno == 2:
			print("Could not open/read file:",remote_config,"using local")
		elif e.errno == 112:
			print("Host is down:",remote_config,"using local")
		else:
			print(e)

	if fetchConfig != "null":

		y = fetchConfig

	else:
		with open(default_config, 'r') as default_config:
			print("Default Config found")
			localConfig = json.load(default_config)
		y = localConfig

	# the result is a Python dictionary:

	configLength = len(y["data"])

	print("Config found",configLength, "devices")

	for i in range(len(y["data"])):
		print("NAME:",y["data"][i]["Name"])
		print("URL:",y["data"][i]["Address"][0]["URL"])
		print("IP:",y["data"][i]["Address"][1]["IP"])
		print("Fan:",y["data"][i]["Fan"])
	# send json to main
	return (y["data"])