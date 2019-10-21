import json

_CREDENTIAL_FILE_NAME = 'Twitter/twitter_credentials.json'


class Credentials:

    def __init__(self):
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_secret = None
        self.get_credentials()

    def get_credentials(self):
        with open(_CREDENTIAL_FILE_NAME, 'r') as json_file:
            credentials = json.load(json_file)

        self.consumer_key = credentials['CONSUMER_KEY']
        self.consumer_secret = credentials['CONSUMER_SECRET']
        self.access_token = credentials['ACCESS_TOKEN']
        self.access_secret = credentials['ACCESS_SECRET']

