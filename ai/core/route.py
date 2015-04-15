# Rushy Panchal
# ai/core/route.py

import json

from core.response import Response
from core.errors import MalformedQuery

def routeRequest(engine, data):
	'''Routes the request'''
	try:
		data = json.loads(data)
		msg_id = data["msg_id"]
	except ValueError:
		return "", Response.error(MalformedQuery("JSON could not be decoded"))
	except KeyError:
		return "", Response.error(MalformedQuery("msg_id field could not be found"))

	try:
		response = ROUTES[data["action"]](engine, data["data"])
		return msg_id, response
	except KeyError:
		return msg_id, Response.error(MalformedQuery("action or data field not provided"))
