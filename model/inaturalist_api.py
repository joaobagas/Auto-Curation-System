import json

import requests

from domain.observation import Observation
from model import user_service
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
    response = requests.post(("%s/oauth/token" % url), payload)
    data = json.loads(response.content)
    UserService.__new__(UserService).set_user_info(username, data["access_token"])


def post_observation(obs):
    requests.post(url + "/observation", allow_redirects=False, data={
        "species_guess": obs.species_guess,
        "taxon_id": "",
        "observed_on_string": "",
        "time_zone": "",
        "description": "",
        "tag_list": "",
        "place_guess": "",
        "latitude": "",
        "longitude": "",
        "map_scale": "",
        "positional_accuracy": "",
        "geoprivacy": "",
        "observation_field_values_attributes": "",
        "flickr_photos": [],
        "picasa_photos": [],
        "facebook_photos": [],
        "local_photos": []
    })
