import requests

from domain.observation import Observation

url = "https://www.inaturalist.org"


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
