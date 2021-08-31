# This class holds the information of regarding the current user.
# The singleton pattern was used so this class is instantiated only once.


class UserService(object):
    _instance = None
    username = None
    password = None
    access_token = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_user_info(self, username, password, access_token):
        self.username = username
        self.password = password
        self.access_token = access_token

    def get_username(self):
        return self.username

    def get_access_token(self):
        return self.access_token
