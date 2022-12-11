import pyseto
from pyseto import Key
from pyseto.exceptions import DecryptError, EncryptError, SignError, VerifyError
from typing import Union

from taskbay.settings import BASE_DIR


def generate_token(payload: Union[bytes,str,dict]) -> bytes:
    try:
        with open(f"{BASE_DIR}/authentication_app/utils/private_key.pem") as key_file:
            private_key = Key.new(version=4, purpose="public", key=key_file.read())

        token_generated = pyseto.encode(key=private_key, payload=f"{payload}")
        return token_generated
    except (ValueError, EncryptError, SignError, IOError) as e:
        return None


def authenticate_token(token: bytes) -> bytes or str:
    try:
        with open(f"{BASE_DIR}/authentication_app/utils/public_key.pem") as key_file:
            public_key = Key.new(version=4, purpose="public", key=key_file.read())

        decoded_message = pyseto.decode(keys=public_key, token=token)
        return decoded_message.payload
    except (ValueError, DecryptError, VerifyError, IOError) as e:
        return None
