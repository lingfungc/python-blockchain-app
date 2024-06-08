import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """
    Hashes a block and returns a string (hashed / encrypted).

    Arguments:
        :block: The block that should be hashed.

    Functions:
        :hashlib.sha256(): Creates a SHA-256 hash object
        :json.dumps(): Converts a Python object into a JSON-formatted string
        :encode(): Encodes the JSON-formatted string into bytes (because SHA-256 hashing function requires a bytes-like object, but not string)
        :hexdigest(): Returns a hexadecimal string (readable)
    """
    # For now, this is only getting the values by the keys in each block and join them with a '-'
    # return '-'.join([str(block[key]) for key in block])

    # The 'sort_keys' here is to make sure the order for the hash is always the same, prevent hashing error (same input)

    # After implementing the Block class, we need to convert the Block instance into dictionary data type
    # In order to get the 'json.dumps()' working for the Block instance

    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())

    # return hash_string_256(json.dumps(block, sort_keys=True).encode())
