from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import pickle
import warnings
warnings.filterwarnings('ignore')

# 密码解密函数
def decrypt_password(password: str, token: bytes):
    with open('salt.pkl', "rb") as salt_file:
        salt= pickle.load(salt_file)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)
    decrypted = f.decrypt(token)
    return decrypted.decode()

# 从文件中读取信息
def read_from_file(filename):
    try:
        with open(filename, "rb") as key_file:
            return pickle.load(key_file)
    except FileNotFoundError as e:
        print('没找到\'key.pkl\'文件')
        exit()


# 从文件中读取加密的密钥
encrypted_key = read_from_file('key.pkl')

# 输入密码
password = input("请输入解密密钥需要的口令: ")

# 解密密钥
try:
    decrypted_key = decrypt_password(password, encrypted_key)
    print(f'密码是: {decrypted_key}')
except Exception:
    print('口令不对.')