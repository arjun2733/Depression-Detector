import binascii
from Cryptodome.Cipher import AES
from Cryptodome import Random
from Cryptodome.Protocol.KDF import PBKDF2

def get_private_key(password):
    salt = b"weal-o-code"
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key

def encrypt(passwrd, message):
    msglist = []
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(bytes(message, "utf-8"))
    msg = binascii.hexlify(msg)
    for letter in str(msg):
        msglist.append(letter)
    msglist.remove("b")
    msglist.remove("'")
    msglist.remove("'")
    encryptedMsg=""
    for letter in msglist:
        encryptedMsg+=letter
    return encryptedMsg

def decrypt(passwrd, message):
    msglist = []
    key = get_private_key(passwrd)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = cipher.decrypt(binascii.unhexlify(bytes(message, "utf-8")))[len(iv):]
    for letter in str(msg):
        msglist.append(letter)
    msglist.remove("b")
    msglist.remove("'")
    msglist.remove("'")
    decMsg=""
    for letter in msglist:
        decMsg+=letter
    return decMsg

passage=input("enter how you are feeling todayyy!: ")
password1=input("enter password: ")
generated_key=get_private_key(password1)
encrypted_message=encrypt(password1,passage)
print(encrypted_message)
decrypted_message=decrypt(password1,encrypted_message)
print(decrypted_message)