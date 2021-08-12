class UserService(object):
    __instance = None
    access_token = None
    username = None

    @staticmethod
    def get_instance():
        if UserService.__instance is None:
            UserService()
        return UserService.__instance

    def __init__(self):
        # Virtually private constructor.
        if UserService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UserService.__instance = self

    def set_user_details(self, access_token, username):
        self.access_token = access_token
        self.username = username
