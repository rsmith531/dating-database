import string
import random
import hashlib

def to_bytes(s):
    return s.encode("utf-8")

def to_string(b):
    return b.decode("utf-8")

def hash_sha256(password, n=1):
    """ was industry standard for a very long time.
    """
    # rehash the string n times to increase cracking time
    for i in range(0, n):
        pass_bytes = password.encode('utf-8')  # convert ascii to utf-8
        sha256 = hashlib.sha256()  # create a sha256 hashing object
        sha256.update(pass_bytes)  # hash the utf-8 to the sha256 standard
        hashed_password = sha256.hexdigest()  # hashed bytes go to a string
    return hashed_password
    
def random_string(length):
    """ This generates a random string to use as a salt,
        which makes hashed passwords virtually impossible
        to decode by analyzing trends in the hash.
    """
    chars = string.ascii_letters + string.digits  # a container of all chars
    choices = random.choices(chars, k=length)  # choose k amt of random chars
    result = ''.join(choices) # put the list into a string
    return result
    
i = int(input("How many passwords do you need: "))
    
for i in range(0, i):
    pass1 = random_string(8)
    salt = random_string(20)

    print(f'\ncleartext password: {pass1}')
    print(f'ciphertext password: {hash_sha256(pass1 + salt, 100)}')
    print(f'salt: {salt}')
