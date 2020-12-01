def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise RuntimeError('Modular inverse of {a} mod {m} does not exist.'.format(a=a, m=m))
    else:
        return x % m
