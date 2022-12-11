class SignInRequest:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class SignInResponse:
    def __init__(self, message, token):
        self.message = message
        self.token = token

class SignUpResponse:
    def __init__(self, message):
        self.message = message
        