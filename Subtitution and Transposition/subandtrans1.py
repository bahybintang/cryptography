#!/usr/bin/python3
import math

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 "


def generateKey(key):
    # subKey is the key for subtitutions
    # transKey is the key for transposition
    subKey = key
    transKey = 0

    # Generate transKey by xor and modulo 7
    for ch in key:
        transKey = transKey ^ ord(ch) % max(7, len(key) // 3)

    # Add 1 so transKey cannot be 0
    transKey += 1

    return subKey, transKey


def encryptVigenere(plaintext, key):
    c = ""

    # Ci = (Mi + Ki) % len(letters)
    for i in range(len(plaintext)):
        c += letters[
            (letters.index(plaintext[i]) +
             letters.index(key[i % len(key)])) % len(letters)
        ]
    return c


def decryptVigenere(plaintext, key):
    d = ""

    # Mi = (Ci - Ki) % len(letters)
    # Don't need Mi = (Ci - Ki + len(letters)) % len(letters)
    # because Python already supported modulus
    # on negative number
    for i in range(len(plaintext)):
        d += letters[
            (letters.index(plaintext[i]) -
             letters.index(key[i % len(key)])) % len(letters)
        ]
    return d


def encryptTranspose(plaintext, key):
    c = ""
    colNum = key
    rowNum = len(plaintext) // key
    for i in range(colNum):
        for j in range(rowNum):
            c += plaintext[j * colNum + i]
    return c


def decryptTranspose(plaintext, key):
    d = ""

    # Flipped column and row in encrypt
    colNum = len(plaintext) // key
    rowNum = key
    for i in range(colNum):
        for j in range(rowNum):
            d += plaintext[j * colNum + i]
    return d


def encrypt(plaintext, key):
    # Getting the key
    subKey, transKey = generateKey(key)

    # Normalize string
    plaintext += "x" * (transKey - (len(plaintext) %
                                    transKey if len(plaintext) % transKey != 0 else transKey))
    return encryptTranspose(encryptVigenere(plaintext, subKey), transKey)


def decrypt(plaintext, key):
    # Getting the key
    subKey, transKey = generateKey(key)

    return decryptVigenere(decryptTranspose(plaintext, transKey), subKey)


if __name__ == '__main__':
    plaintext = input("Plaintext: ")
    key = input("Key: ")
    cipher = encrypt(plaintext, key)
    decipher = decrypt(cipher, key)
    print("Encrypted: ", cipher)
    print("Decrypted: ", decipher)
