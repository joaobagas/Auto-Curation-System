# This files holds all the API calls needed for the system to work and the information necessary to perform them.

import json

import requests

from model.user_service import UserService

url = "https://www.inaturalist.org"
app_id = "b974e28242fd352e2fc32defab55390e7580f0ac36d4e7bd23957d8e1f05e55a"
app_secret = "b038d5b2e158c822f1b2645a3777b6449b97dbce96c70dc4d9a07ef4b17a0788"


def login(username, password):
    payload = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': "password",
        'username': username,
        'password': password
    }
    response = requests.post((url + "/oauth/token"), payload)

    if response.status_code == 200:
        data = json.loads(response.content)
        UserService.__new__(UserService).set_user_info(username, password, data["access_token"])


def post_observation(obs):
    head = {'Authorization': 'Bearer ' + UserService.__new__(UserService).get_access_token()}
    payload = {
        "species_guess": obs.species_guess,
        "taxon_id": obs.taxon_id,
        "observed_on_string": obs.observed_on_string,
        "time_zone": obs.time_zone,
        "description": obs.description,
        "tag_list": obs.tag_list,
        "place_guess": obs.place_guess,
        "latitude": obs.latitude,
        "longitude": obs.longitude,
        "map_scale": obs.map_scale,
        "positional_accuracy": obs.positional_accuracy,
        "geoprivacy": obs.geoprivacy,
        "observation_field_values_attributes": obs.observation_field_values_attributes,
        "flickr_photos": obs.flickr_photos,
        "picasa_photos": obs.picasa_photos,
        "facebook_photos": obs.facebook_photos,
        "local_photos": obs.local_photos
    }
    response = requests.post(url + "/observations", allow_redirects=False, json=payload, headers=head)

    if response.status_code == 200:
        print("Success!")
    else:
        print(response)
