import json
import os
# import jwtGenerator_symmetric
import pymongo
from bson import ObjectId
from bson.json_util import dumps
from flask import Blueprint, request, jsonify
import jwt
import os
import datetime
import sys

# import pathlib


class JSONEncoder(json.JSONEncoder):
	"""
	Extend JSON Encoder to support mongoDB id encoding
	"""
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)

API_KEY = os.environ.get('API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_INITDB_ROOT_USERNAME = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')

if not API_KEY:
    raise ValueError("API_KEY is not set.")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set.")

	
def encode_auth_token(e_message, e_to, e_from, e_timeToLifeSec, my_secret):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            "message" : e_message,
            "to": e_to,
            "from": e_from,
            "timeToLifeSec" : int(e_timeToLifeSec)
            #For a more secured way, used this payload
            
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            # 'iat': datetime.datetime.utcnow(),
            # 'sub': user_nickname
            
            #For the interview process purpose, it will be used this unsafe way. In this way the interviewer can test the solution
            # "sub": user_nickname
        }
        text =""
        text += str(jwt.encode(
            payload,
            my_secret,
            algorithm = 'HS256'
        ))
        return text
    except Exception as e:
        return e

class MongoProvider(object):
    

	def __init__(self):
		"""
		Create the connection with mongoDB
		"""
		# self.myclient = pymongo.MongoClient(f'mongodb://admin:admin@'+os.environ.get('MONGO_INITDB_ROOT_USERNAME')+':'+os.environ.get('MONGO_INITDB_ROOT_PASSWORD')+'@'+os.environ.get('MONGO_URL')+':'+os.environ.get('MONGO_PORT')+'/')
		#pymongo.MongoClient(f"<linux_mongosh_COMMAND")
		self.myclient = pymongo.MongoClient(f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{os.environ.get('MONGO_URL')}:{os.environ.get('MONGO_PORT')}/")
		self.mydb = self.myclient["MyProject"]
		self.mycol = self.mydb["messages"]

	main = Blueprint('main', __name__)
	
	
	def generate_jwt_endpoint(self): 
				
		received_api_key = request.headers.get("X-Parse-REST-API-Key")

		if received_api_key == None or received_api_key == "":
			return "ERROR: Invalid API Key", 401

		else:

			if str(received_api_key) == API_KEY:       

				token =""
					# encode_   auth_token(e_message, e_to, e_from, e_timeToLifeSec, my_secret)
				token += (encode_auth_token("-", "-", MONGO_INITDB_ROOT_USERNAME, "-1", SECRET_KEY)).__str__() 
				print(token)
				
				return token
			else:
				return "ERROR: You need Admin permissions", 401

	
	# def get_secret(user) -> str:
	# 	return f"You are {user} and the secret is 'wbevuec'"
	
	
	def create_message(self, payload):
		
		received_api_key = request.headers.get("X-Parse-REST-API-Key")

		if received_api_key == None or received_api_key == "":
			return "Empty received_api_key"
		
		if API_KEY == None or API_KEY == "":
			return "Empty API_KEY"
			
		if not received_api_key == API_KEY:
			print("Received API Key: {received_api_key}")
			return "ERROR: Invalid API Key", 401
	
		jwt_header = request.headers.get("X-JWT-KWY")
		if not jwt_header:
			return "ERROR: Missing JWT Header", 400
		try:
			JWT_TOKEN = self.generate_jwt_endpoint()
			# print(jwt_header)
			# print(SECRET_KEY)
			decoded_payload = jwt.decode(JWT_TOKEN, SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			return "ERROR: JWT Token has expired", 401
		except jwt.InvalidTokenError:
			return "ERROR: Invalid JWT Token", 401

		if decoded_payload["from"] != MONGO_INITDB_ROOT_USERNAME:
			return "ERROR: Unauthorized user", 401

		"""
		Create a message with the information provided in the payload
		:param payload: dict
			Dictionary passed as input
		:return: (dict, int)
			Response JSON, Error code
		"""
		if self.mycol.count_documents({'timeToLifeSec': payload['timeToLifeSec']}, limit=1) != 0:

			return {"error": "Found message with existing Time To Life Sec"}, 409
			
		else:
			self.mycol.insert_one(payload)
			return { 'message' : ('Hello '+ payload['to' ] + ', your message will be sent' )}, 201

	def read_message(self):
		messageTimeToLifeSec = request.headers.get("messageTimeToLifeSec")
		# if messageTimeToLifeSec == None or messageTimeToLifeSec == "":
		# 	return "Empty received_api_key"
		# else:

		"""
		Read a message from the database given its timeToLifeSec
		:param messageTimeToLifeSec: int
			TimeToLifeSec of the message
		:return: (dict, int)
			Response JSON, Error code
		"""
		# if self.mycol.count_documents({'timeToLifeSec': int(messageTimeToLifeSec)}, limit=1) != 0:
		# 	message_query = {"timeToLifeSec": messageTimeToLifeSec}

		# 	message = self.mycol.find_one(message_query)
		# 	message = JSONEncoder().encode(message)
		# 	return json.loads(message), 200
		message_query = {"timeToLifeSec": int(messageTimeToLifeSec)}
		message = self.mycol.find_one(message_query)
		if message != None:
	# if self.mycol.count_documents({'timeToLifeSec': int(messageTimeToLifeSec)}, limit=1) != 0:
			message = JSONEncoder().encode(message)
			return json.loads(message), 200
		else:
			return {"error": "message not found"}, 400

	def update_message(self, payload):
    
		received_api_key = request.headers.get("X-Parse-REST-API-Key")

		if received_api_key == None or received_api_key == "":
			return "Empty received_api_key: " + received_api_key
		
		if API_KEY == None or API_KEY == "":
			return "Empty API_KEY"
			
		if not received_api_key == API_KEY:
			print("Received API Key: {received_api_key}")
			return "ERROR: Invalid API Key", 401
	
		jwt_header = request.headers.get("X-JWT-KWY")
		if not jwt_header:
			return "ERROR: Missing JWT Header", 400
		try:
			JWT_TOKEN = self.generate_jwt_endpoint()
			# print(jwt_header)
			print(SECRET_KEY)
			decoded_payload = jwt.decode(JWT_TOKEN, SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			return "ERROR: JWT Token has expired", 401
		except jwt.InvalidTokenError:
			return "ERROR: Invalid JWT Token", 401

		if decoded_payload["from"] != MONGO_INITDB_ROOT_USERNAME:
			return "ERROR: Unauthorized user", 401

		"""
		Update a message with the information provided in the payload
		:param payload: dict
			Dictionary passed as input
		:return: (dict, int)
			Response JSON, Error code
		"""
		# messageTimeToLifeSec = request.headers.get("messageTimeToLifeSec")

		# if messageTimeToLifeSec == None or messageTimeToLifeSec == "":
		# 	return "Empty messageTimeToLifeSec"
		# else:
		if self.mycol.count_documents({'timeToLifeSec': int(payload['timeToLifeSec'])}, limit=1) != 0: # Check if message exists in DB
			print("Found a message in DB with this timeToLifeSec")
			message_query = {"timeToLifeSec": int(payload['timeToLifeSec'])}
			new_values = {"$set": payload}

			x = self.mycol.update_one(message_query, new_values)
			if x.modified_count != 0:
				return {"message": "Success"}, 201
			else:
				return {"error": "Message not modified. Change any value you try to update."}, 403
		else:
			return {"error": "message not found"}, 409

	def delete_message(self):
    
		messageTimeToLifeSec = request.headers.get("messageTimeToLifeSec")
		if messageTimeToLifeSec == None or messageTimeToLifeSec == "":
			return "The time to life sec was never received"
		
		received_api_key = request.headers.get("X-Parse-REST-API-Key")

		if received_api_key == None or received_api_key == "":
			return "Empty received_api_key"
		
		if API_KEY == None or API_KEY == "":
			return "Empty API_KEY"
			
		if not received_api_key == API_KEY:
			print("Received API Key: {received_api_key}")
			return "ERROR: Invalid API Key", 401
	
		jwt_header = request.headers.get("X-JWT-KWY")
		if not jwt_header:
			return "ERROR: Missing JWT Header", 400
		try:
			JWT_TOKEN = self.generate_jwt_endpoint()
			# print(jwt_header)
			print(SECRET_KEY)
			decoded_payload = jwt.decode(JWT_TOKEN, SECRET_KEY, algorithms=["HS256"])
		except jwt.ExpiredSignatureError:
			return "ERROR: JWT Token has expired", 401
		except jwt.InvalidTokenError:
			return "ERROR: Invalid JWT Token", 401

		if decoded_payload["from"] != MONGO_INITDB_ROOT_USERNAME:
			return "ERROR: Unauthorized user", 401

		"""
		Delete a message from the database given its timeToLifeSec
		:param messageTimeToLifeSec: int
			TimeToLifeSec of the message
		:return: (dict, int)
			Response JSON, Error code
		"""
		# if messageTimeToLifeSec != "" or messageTimeToLifeSec != None:
		message_query = {"timeToLifeSec": int(messageTimeToLifeSec)}
		x = self.mycol.delete_one(message_query)
		if x.deleted_count != 0:
			return {"message": "Success"}, 200

		else:
			return {"error": "message not found"}, 400
		# else:
		# 	return {"error": "time to life sec variabled not typed"}, 400
