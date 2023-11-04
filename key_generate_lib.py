from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import random
import string
import time
import pickle
import warnings
warnings.filterwarnings('ignore')

# 生成随机密钥
def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# 密码加密函数
def encrypt_password(password: str, message: str):
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
    encrypted = f.encrypt(message.encode())
    return encrypted

# 写入文件的函数
def write_to_file(filename, content):
    with open(filename, "wb") as key_file:
        pickle.dump(content, key_file)

# 后台线程执行的任务
def task(duration,encrypted_key):
    time.sleep(duration) # 等待秒数
    write_to_file('key.pkl', encrypted_key)
