from flask import Blueprint, render_template, redirect, request
import requests
from oauthlib.oauth2 import WebApplicationClient
from os import environ
import json

auth_blueprint = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration")

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@auth_blueprint.route("/login")
def login():
  google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
  authorization_endpoint = google_provider_cfg["authorization_endpoint"]

  request_uri = client.prepare_request_uri(
      authorization_endpoint,
      redirect_uri=request.host_url + "authorize",
      scope=["openid", "email", "profile"],
  )

  return redirect(request_uri)


@auth_blueprint.route("/authroize")
def authorize():
  code = request.args.get("code")
  google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
  token_endpoint = google_provider_cfg["token_endpoint"]
  token_url, headers, body = client.prepare_token_request(
      token_endpoint,
      authorization_response=request.url,
      redirect_url=request.base_url,
      code=code)
  token_response = requests.post(token_url,
                                 headers=headers,
                                 data=body,
                                 auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET))

  print(token_response.json())
  client.parse_request_body_response(json.dumps(token_response.json()))

  # Now that we have the token, let's find and return the profile info
  userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
  uri, headers, body = client.add_token(userinfo_endpoint)
  userinfo_response = requests.get(uri, headers=headers, data=body)

  # The userinfo_response object contains the user's information
  print(userinfo_response.json())

  return "OK"
