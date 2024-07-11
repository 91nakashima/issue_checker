from jwt import JWT, jwk_from_pem
import time
import os


def create_jwt():

    pem = './private-key.pem'

    # Get the Client ID
    client_id = os.getenv("GITHUB_APP_CLIENT_ID")

    # Open PEM
    with open(pem, 'rb') as pem_file:
        signing_key = jwk_from_pem(pem_file.read())

    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,

        # GitHub App's client ID
        'iss': client_id
    }

    # Create JWT
    jwt_instance = JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

    return encoded_jwt
