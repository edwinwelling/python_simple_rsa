from math import gcd
from random import shuffle


class RSAPrivateKey:

    def __init__(self, d: int, n: int):
        self.d = d
        self.n = n

    def decrypt(self, encrypted_msg: list[int]):
        return "".join([chr(pow(val, self.d, self.n)) for val in encrypted_msg])

    def __str__(self):
        return f"(d:{self.d}, n:{self.n})"


class RSAPublicKey:
    def __init__(self, e: int, n: int):
        self.e = e
        self.n = n

    def encrypt(self, msg: str) -> list[int]:
        return [pow(ord(c), self.e, self.n) for c in msg]

    def __str__(self):
        return f"(e:{self.e}, n:{self.n})"


class RSA:

    def __init__(self, p: int, q: int):
        self.n = p * q
        self.phi = (p - 1) * (q - 1)

        self.shuffled_range = list(range(2, self.phi))
        print(f"shuffle range (2,{self.phi}]")
        shuffle(self.shuffled_range)

        self.e = 0
        self.d = 0

        self.__search_public_exponent()
        self.__search_private_exponent()

    def __search_private_exponent(self):
        for self.d in self.shuffled_range:
            if (self.e * self.d) % self.phi == 1:
                break

    def __search_public_exponent(self):
        for self.e in self.shuffled_range:
            if gcd(self.e, self.phi) == 1:
                break

    def get_public_key(self) -> RSAPublicKey:
        return RSAPublicKey(self.e, self.n)

    def get_private_key(self) -> RSAPrivateKey:
        return RSAPrivateKey(self.d, self.n)


if __name__ == '__main__':
    rsa = RSA(1427, 2423)

    message = "Atvin is my Starbucks name"
    public_key = rsa.get_public_key()
    print(f"Alice encrypt message: '{message}' with public key: {public_key}")

    secret = public_key.encrypt(message)
    print(f"Alice send {secret} to Bob")

    private_key = rsa.get_private_key()
    decrypted = private_key.decrypt(secret)
    print(f"Bob decrypt to '{decrypted}' using private key: {private_key}")
