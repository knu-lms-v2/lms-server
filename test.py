import os
from cryptography.fernet import Fernet

key = os.environ['FERNET_KEY']
f = Fernet(key)