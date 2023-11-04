from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import threading
import random
import string
import time
import pickle
import atexit
import warnings
import readchar
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
def task(duration):
    global saved
    time.sleep(duration) # 等待秒数
    write_to_file('key.pkl', encrypted_key)
    print(f'密码已经保存到文件.')
    saved=True

#生成密码
key = generate_key()
encrypted_key = encrypt_password('pwd123', key)  # 使用'pwd123'作为密码
print(f'密码 {key} 已生成并加密，等待保存到文件，请注意，密码将只显示一次，请按回车继续.', end='',flush=True)
while True:
    user_input = readchar.readchar()
    if user_input == '\r':  # 检查是否是回车键
        break
    else:
        print('\r' + ' ' * 100) 
        print('\n未保存到文件，将退出')
        exit()

print('\r' + ' ' * 100) 


# 创建守护线程
daemon_thread = threading.Thread(target=task, kwargs={"duration": 24 * 60 * 60},name='DaemonThread', daemon=True)
saved=False

# 注册退出处理函数
def exit_handler():
    if encrypted_key is not None and saved==False:
        write_to_file('key.pkl', encrypted_key)
        print(f'密码已经保存到文件.')

atexit.register(exit_handler)

daemon_thread.start()

# 主线程等待10秒，给守护线程足够的时间来运行
while(True):
    time.sleep(10)
