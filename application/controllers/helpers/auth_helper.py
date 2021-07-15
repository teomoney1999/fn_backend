import random, string


def generator_salt():
    data = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))
    return str(data)