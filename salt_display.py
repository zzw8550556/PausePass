import pickle

with open('salt.pkl', "rb") as salt_file:
    salt= pickle.load(salt_file)

print(f'盐值为：{salt}.')