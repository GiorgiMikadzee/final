from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_pad
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as aes_pad
import os

# --- Key setup ---
key_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
key_pub = key_priv.public_key()

with open("private.pem", "wb") as f:
    f.write(key_priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ))

with open("public.pem", "wb") as f:
    f.write(key_pub.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# --- Alice's message ---
msg = b"Bob you are my crush!"
with open("alice_message.txt", "wb") as f:
    f.write(msg)

# --- AES encryption ---
aes_k = os.urandom(32)
aes_iv = os.urandom(16)

padder = aes_pad.PKCS7(128).padder()
padded_msg = padder.update(msg) + padder.finalize()

aes_cipher = Cipher(algorithms.AES(aes_k), modes.CBC(aes_iv)).encryptor()
aes_encrypted = aes_cipher.update(padded_msg) + aes_cipher.finalize()

with open("encrypted_file.bin", "wb") as f:
    f.write(aes_iv + aes_encrypted)

# --- Encrypt AES key with RSA ---
aes_k_enc = key_pub.encrypt(
    aes_k,
    rsa_pad.OAEP(mgf=rsa_pad.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)
with open("aes_key_encrypted.bin", "wb") as f:
    f.write(aes_k_enc)

# --- Decrypt AES key ---
with open("aes_key_encrypted.bin", "rb") as f:
    aes_k_dec = key_priv.decrypt(f.read(), rsa_pad.OAEP(mgf=rsa_pad.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# --- Decrypt file ---
with open("encrypted_file.bin", "rb") as f:
    iv = f.read(16)
    cdata = f.read()

dec_cipher = Cipher(algorithms.AES(aes_k_dec), modes.CBC(iv)).decryptor()
dec_padded = dec_cipher.update(cdata) + dec_cipher.finalize()

unpadder = aes_pad.PKCS7(128).unpadder()
plaintext = unpadder.update(dec_padded) + unpadder.finalize()

with open("decrypted_message.txt", "wb") as f:
    f.write(plaintext)

# --- SHA-256 check ---
h1 = hashes.Hash(hashes.SHA256()); h1.update(msg)
h2 = hashes.Hash(hashes.SHA256()); h2.update(plaintext)

assert h1.finalize() == h2.finalize(), "Hash mismatch!"
print("✔ Message integrity verified.")