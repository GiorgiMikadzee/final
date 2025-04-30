This project demonstrates a hybrid encryption setup using RSA and AES for secure file sharing.

Alice creates a message ("Bob you are my crush!") and writes it to alice_message.txt. 
She encrypts the message using AES-256 with a randomly generated key and IV, storing the result in encrypted_file.bin. 
Then, she encrypts the AES key using Bob’s RSA public key, and saves it in aes_key_encrypted.bin.

Bob uses his RSA private key to decrypt the AES key and uses it with the IV to decrypt the file. 
The output is saved in decrypted_message.txt. 
A SHA-256 hash comparison is used to confirm that the decrypted message matches the original.

Files included:

Final_Task-2_Mikadze.py — Python code

alice_message.txt — original message

encrypted_file.bin — AES encrypted file with IV

aes_key_encrypted.bin — RSA-encrypted AES key

decrypted_message.txt — decrypted message

public.pem, private.pem — Bob's RSA key pair

This example shows how real secure systems exchange messages using fast symmetric encryption for data and public-key encryption for secure key sharing.

