# This files holds all the API calls needed for the system to work and the information necessary to perform them.

import base64

from pyinaturalist import *

from model.user_service import UserService

url = "https://www.inaturalist.org"
app_id = "b974e28242fd352e2fc32defab55390e7580f0ac36d4e7bd23957d8e1f05e55a"
app_secret = "b038d5b2e158c822f1b2645a3777b6449b97dbce96c70dc4d9a07ef4b17a0788"

def login(usrnm, pswrd):
    token = get_access_token(usrnm, pswrd, app_id, app_secret)
    UserService.__new__(UserService).set_user_info(usrnm, pswrd, token)
    print(token)

def post_observation():
    photos = ['img/observations/nc.jpg', 'img/observations/1.Lion-acs-1005.jpg']
    response = create_observation(
        access_token=UserService.__new__(UserService).get_access_token(),
        species_guess="Northern Cardinal",
        taxon_id="9083",
        photos=photos
    )
    print(response)

