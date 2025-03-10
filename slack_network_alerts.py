from error_codes import error_codes
import json
import sys
import random
import re
import requests

def slack(title,output=''):
	url = "https://hooks.slack.com/services/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"
	message = output
	slack_data = {
		"username": "NotificationBot",
		"icon_emoji": ":satellite:",
		"blocks": [
				{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*{}*\n{}".format(title,message)
				}
			}
		]
	}
	byte_length = str(sys.getsizeof(slack_data))
	headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
	response = requests.post(url, data=json.dumps(slack_data), headers=headers)
	if response.status_code != 200:
		raise Exception(response.status_code, response.text)
