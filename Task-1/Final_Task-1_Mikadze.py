# encrypted_messaging_app.py (Lab 6 Padding Oracle style)

from cryptography.hazmat.primitives import padding as sympad
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsapad
from cryptography.hazmat.primitives import serialization, hashes
from binascii import hexlify, unhexlify
import os

BLOCK_SIZE = 16

# Simulated shared message
MESSAGE = b"Bilbo Baggins had the Ring"

# === User A: RSA key generation ===
priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub_key = priv_key.public_key()

# === User B: AES encryption ===
aes_key = os.urandom(32)
iv = os.urandom(BLOCK_SIZE)
padder = sympad.PKCS7(128).padder()
padded = padder.update(MESSAGE) + padder.finalize()
cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded) + encryptor.finalize()

# === User B: Encrypt AES key with RSA ===
aes_key_encrypted = pub_key.encrypt(
    aes_key,
    rsapad.OAEP(mgf=rsapad.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# === Save files ===
open("message.txt", "wb").write(MESSAGE)
open("encrypted_message.bin", "wb").write(iv + ciphertext)
open("aes_key_encrypted.bin", "wb").write(aes_key_encrypted)

# === User A: Decrypt AES key ===
with open("aes_key_encrypted.bin", "rb") as f:
    aes_key = priv_key.decrypt(
        f.read(),
        rsapad.OAEP(mgf=rsapad.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

# === User A: Decrypt message ===
with open("encrypted_message.bin", "rb") as f:
    iv = f.read(BLOCK_SIZE)
    ciphertext = f.read()

decipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv)).decryptor()
padded_plain = decipher.update(ciphertext) + decipher.finalize()
unpadder = sympad.PKCS7(128).unpadder()
plaintext = unpadder.update(padded_plain) + unpadder.finalize()

open("decrypted_message.txt", "wb").write(plaintext)
