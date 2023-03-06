import random
import string

def generate_short_id(size=10, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))
