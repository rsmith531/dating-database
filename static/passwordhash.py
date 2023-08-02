''' password hashing helper functions

    Developed by:
        Sidney R
        Dennis S
        Ryan S
        Eric S
        Erik Z

    For:
        CS 33007 Database Systems
        Summer 2023
        Kent State University
'''

import string
import random
import hashlib

def make_salt(length):
    """ This generates a random string to use as a salt,
        which makes hashed passwords virtually impossible
        to decode by analyzing trends in the hash.
    """
    chars = string.ascii_letters + string.digits  # a container of all chars
    choices = random.choices(chars, k=length)  # choose k amt of random chars
    result = ''.join(choices) # put the list into a string
    return result

def hash_sha256(password, salt=make_salt(20), rounds=100):
    """ hash a password n times with the SHA 256 algorithm
        parameters: a cleartext password, number of hash rounds
        returns: tuple of (hashed_password, salt)
    """

    to_hash = password + salt

    # rehash the string n times to increase cracking time
    for i in range(0, rounds):
        pass_bytes = to_hash.encode('utf-8')  # convert ascii to utf-8
        sha256 = hashlib.sha256()  # create a sha256 hashing object
        sha256.update(pass_bytes)  # hash the utf-8 to the sha256 standard
        hashed_password = sha256.hexdigest()  # hashed bytes go to a string

    return (hashed_password, salt)
