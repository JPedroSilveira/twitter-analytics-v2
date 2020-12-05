Twitter Analytics 2
College project to apply file manipulation techniques.

This project use pipenv to simplify the management of dependencies.
    - Before run:
        - pipenv shell
        - pipenv install
    - To run:
        - pipenv run python Main.py
    - Pipenv doc: https://pipenv-fork.readthedocs.io/en/latest/

To execute in command line use (in main repository):
    python Main.py

You need Python 3.8 installed to run this project

To use Twitter Streamer function (search for new tweets) you will need to create a twitter developer account (https://developer.twitter.com/en/apply-for-access). Create a JSON file named "twitter_credentials.json" in Twitter folder with the following format:
{"CONSUMER_KEY": "Put your consumer key here", "CONSUMER_SECRET": "Put your consumer secret here", "ACCESS_TOKEN": "Put your access token here", "ACCESS_SECRET": "Put your access secret here" }
