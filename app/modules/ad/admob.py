from datetime import datetime, timedelta
import json
import urllib.parse

from base64 import urlsafe_b64decode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import requests

from app.error.bad_request_exception import BadRequestException
from config import settings

# Global cache for the public key
public_key_cache = {
    "key": None,
    "expires_at": None
}

def get_cached_public_key(key_id: int):
    global public_key_cache

    # Check if the cached key is still valid
    if public_key_cache["key"] and public_key_cache["expires_at"] > datetime.now():
        return public_key_cache["key"]

    # Fetch the public key from the remote URL
    public_key_url = settings.admob_public_key_url
    public_key_data = requests.get(public_key_url).text
    public_key_json = json.loads(public_key_data)
    public_keys = public_key_json['keys']

    # Find the public key with the matching key ID
    public_key = None
    for key in public_keys:
        if key['keyId'] == key_id:
            public_key = key
            break
    if public_key is None:
        raise BadRequestException("Public key not found for the given key ID.")

    # Extract the public key in PEM format
    public_key_pem = public_key['pem'].replace("\\n", "\n").encode('utf-8')
    loaded_public_key = serialization.load_pem_public_key(public_key_pem)

    # Cache the public key for 24 hours
    public_key_cache["key"] = loaded_public_key
    public_key_cache["expires_at"] = datetime.now() + timedelta(hours=24)

    return loaded_public_key

def verify_signature(params: dict, key_id: int, signature: str) -> bool:
    try:
        # Get the public key
        public_key = get_cached_public_key(key_id)
        if not public_key:
            raise Exception("Public key not found.")

        # Fix Base64 URL padding if necessary
        missing_padding = len(signature) % 4
        if missing_padding != 0:
            signature += "=" * (4 - missing_padding)

        # Decode the signature from Base64 URL encoding
        decoded_signature = urlsafe_b64decode(signature)

        # Prepare the signed data (exclude 'signature' key and URL-encode values)
        signed_data = '&'.join([
            f'{k}={urllib.parse.quote(str(v), safe="")}'
            for k, v in sorted(params.items())
            if k not in ('signature', 'key_id')
        ])

        # Verify the signature using ECDSA with SHA256
        public_key.verify(decoded_signature, signed_data.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        return False
