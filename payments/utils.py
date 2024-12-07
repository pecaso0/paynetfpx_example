import base64
from OpenSSL import crypto

def sign_message(message, private_key_path):
    with open(private_key_path, 'r') as key_file:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())
    signature = crypto.sign(private_key, message.encode('utf-8'), 'sha1')
    return base64.b64encode(signature).decode('utf-8')
