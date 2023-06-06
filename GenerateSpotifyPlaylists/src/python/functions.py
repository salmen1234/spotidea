import random
import string

def generateRandomString(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string