from hashlib import md5
from os import urandom


def gen_key():
    return md5(urandom(32)).digest().hex()
