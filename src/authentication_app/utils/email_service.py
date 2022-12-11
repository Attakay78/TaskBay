class EmailService:
    def __init__(self, email, message):
        self.email = email
        self.message =message
    
    def send_mail(self):
        print(self.message)