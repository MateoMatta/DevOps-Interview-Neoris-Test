import os
from flask_injector import inject
from providers.MongoProvider import MongoProvider

data_provider = MongoProvider()

@inject
def create_message(message_payload):
    return data_provider.create_message(message_payload)

@inject
def read_message():
    return data_provider.read_message()

@inject
def update_message(message_payload):
    return data_provider.update_message(message_payload)

@inject
def delete_message():
    return data_provider.delete_message()

@inject
def generate_jwt_endpoint():
    return data_provider.generate_jwt_endpoint()

@inject
def get_secret():
    return data_provider.get_secret()

