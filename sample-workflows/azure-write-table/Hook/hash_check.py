import hashlib
import hmac
import base64
import os

# Pulling a value from the environment allows you to quickly update the secret key
# from within Azure, instead of re-deploying the entire function to update the hardcoded value
#SECRETKEY = os.environ['SECRETKEY'].encode('utf-8')
SECRETKEY = "MYSECRETKEY"

def crc_response(crc):

    payload = str.encode(crc)

    secret = str.encode(SECRETKEY)

    signature = 'sha256=' + base64.b64encode(hmac.new(secret, payload, 
                            digestmod=hashlib.sha256).digest()).decode()
    return signature


def verify(payload, xsigHash):

    secret = str.encode(SECRETKEY)

    signature = 'sha256=' + base64.b64encode(hmac.new(secret, payload, 
                            digestmod=hashlib.sha256).digest()).decode()

    if signature == xsigHash:
        return True
    else:
        return False