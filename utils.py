import hashlib
import json

def encrypt_string(string_message, pub_key):
    """
    Take in a plaintext utf8 string and returns the encrypted bytes
    """
    return rsa.encrypt(string_message, pub_key).encode('utf-8')

def decrypt_bytes(byte_message, priv_key):
    """
    Take in an encrypted byte message and returns the decrypted utf8 string
    """
    return rsa.decrypt(byte_message, priv_key).decode('utf-8')

def md5(fname):
    """
    Returns the hexdigest of the md5 checksum of the specified file
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def jsonify(filename):
    """
    Returns a string representation of the json data about the filename:
    NOTE: actual string, not bytestring
    {
        "filename" : "filename.extension",
        "md5checksum" : "hexdigest"
    }
    """
    json_dict = {
        "filename" : filename.split('/')[-1],
        "md5checksum" : md5(filename) 
    }
    return json.dumps(json_dict)