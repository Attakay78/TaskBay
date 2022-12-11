import base64
import bcrypt
import hashlib

def generate_password_hash(password):
    salt = bcrypt.gensalt()
    # encoded_password = base64.b64encode((hashlib.sha256(password.encode('UTF-8')).digest()))
    hashed_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed_password

def check_password(raw_password, hashed_password):
    if bcrypt.checkpw(raw_password.encode('UTF-8'), hashed_password):
        return True
    return False
