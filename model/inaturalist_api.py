# This files holds all the API calls needed for the system to work and the information necessary to perform them.

import base64

from pyinaturalist import *

from model.user_service import UserService

url = "https://www.inaturalist.org"
app_id = "b974e28242fd352e2fc32defab55390e7580f0ac36d4e7bd23957d8e1f05e55a"
app_secret = "b038d5b2e158c822f1b2645a3777b6449b97dbce96c70dc4d9a07ef4b17a0788"

def login(username, password):
    token = get_access_token(username, password, app_id, app_secret)
    UserService.__new__(UserService).set_user_info(username, password, token)
    print(token)

def post_observation(obs: Observation, photos):
    response = create_observation(
        access_token=UserService.__new__(UserService).get_access_token(),
        species_guess=obs.species_guess,
        taxon_id=obs.taxon_id,
        observed_on_string=obs.observed_on_string,
        time_zone=obs.time_zone,
        place_guess=obs.place_guess,
        latitude=obs.latitude,
        longitude=obs.longitude,
        description=obs.description,
        photos=photos
    )

