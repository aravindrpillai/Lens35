import base64
from cryptography.fernet import Fernet
from util.property_reader import PropertyReader

def encrypt(plain_text):
    key = PropertyReader.get_property("encryption", "key")
    cipher_suite = Fernet(key.encode('utf-8'))
    cipher_text = cipher_suite.encrypt(plain_text.encode('utf-8'))
    cipher_text_b64 = base64.urlsafe_b64encode(cipher_text).decode('utf-8')
    return cipher_text_b64

def decrypt(cipher_text) -> str:
    key = PropertyReader.get_property("encryption", "key")
    cipher_suite = Fernet(key.encode('utf-8'))
    cipher_text_decoded = base64.urlsafe_b64decode(cipher_text)
    plain_text = cipher_suite.decrypt(cipher_text_decoded).decode('utf-8')
    return plain_text
