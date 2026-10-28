from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import hashlib

def get_binary_key(secret_key):
    if isinstance(secret_key, str):
        secret_key = secret_key.encode()
    return hashlib.sha256(secret_key).digest()

def encrypt_file_pipeline(raw_files, secret_key):
    file_bytes = raw_files.read()
    initialization_vector = os.urandom(16)
    
    binary_key = get_binary_key(secret_key)
    cipher_engine = Cipher(algorithms.AES(binary_key), modes.CFB(initialization_vector))
    encryptor = cipher_engine.encryptor()
    scrambeld_data = encryptor.update(file_bytes) + encryptor.finalize()

    final_payload = initialization_vector + scrambeld_data
    return final_payload

def decrypt_file_pipeline(encrpted_payload, secret_key):
    initialization_vector = encrpted_payload[:16]
    scrambled_data = encrpted_payload[16:]

    binary_key = get_binary_key(secret_key)
    cipher_engine = Cipher(algorithms.AES(binary_key), modes.CFB(initialization_vector))
    decryptor = cipher_engine.decryptor()

    return decryptor.update(scrambled_data) + decryptor.finalize()