import os
import pickle

salt = os.urandom(16)
with open('salt.pkl', "wb") as salt_file:
    pickle.dump(salt, salt_file)

print(f'盐{salt}已生成并保存到文件.')