from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


key = b'G\xff\x19\x84\\iO.8\x1dn\n\xb3\xc8b\xe0'  # 16 байт - для AES128
iv = b'\xf3Q\xa7]GS\xae\x07\xd3\x1a\x18mH\x88\r\xc0'  # 16 байт

cipher = Cipher(algorithms.AES128(key), modes.CBC(iv), backend=default_backend())




# pad_data добавляет байты, пока шифр не будет кратным 16 байтам

def pad_data(data: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()  # блок 128 бит = 16 байт
    return padder.update(data) + padder.finalize()

# unpad_data возвращает в исходное состояние шифрованный текст с добавленными байтами

def unpad_data(data: bytes) -> bytes:
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()

# crypting функция шифрования данных, используемая для шифрования данных

def crypting(data: bytes) -> bytes:
    cipher = Cipher(algorithms.AES128(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = pad_data(data)
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted

# decrypting обращает шифрование после функции crypting

def decrypting(crypted_data: bytes) -> str:
    cipher = Cipher(algorithms.AES128(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(crypted_data) + decryptor.finalize()
    unpadded = unpad_data(decrypted_padded)
    return unpadded.decode('utf-8')

