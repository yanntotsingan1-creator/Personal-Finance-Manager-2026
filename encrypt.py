import random
import string

chars = string.ascii_letters + string.digits + string.punctuation + " "
chars = list(chars)
key = chars.copy()
random.shuffle(key)

# Encrypt
message = input("Enter a message to encrypt: ")
encrypted_message = ""
for letter in message:
    index = chars.index(letter)
    encrypted_message += key[index]
print(f'Original message: {message}')
print(f'Encrypted message: {encrypted_message}')

# Decrypt
encrypted_message = input("Enter a message to decrypt: ")
message = ""
for letter in encrypted_message:
    index = key.index(letter)
    message += chars[index]
print(f'Original message: {message}')