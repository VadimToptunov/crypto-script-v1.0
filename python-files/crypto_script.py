# author == "Vadim Toptunov"

import argparse
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os
import random
import re

"""
The script is made to encrypt and decrypt files with options in command line like:

python ./crypto_script.py -d -f 123.pdf -p test

The script is made with the help of Youtube tutorials by DrapsTV:
https://www.youtube.com/channel/UCea5cMUa9xNU0kUtbRcTkqA

Actually, I tok the encryption and decryption part from there, some argparse part also and then rebuilt it for my needs.
"""


def encrypt(key, filename):

#The function takes a file, encrypts it and creates the encrypted file with AES.

    chunksize = 64*1024
    output_file = "encrypted__" + filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ''

    for i in range(16):
        IV += chr(random.randint(0, 0xFF))
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            outfile.write(filesize)
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
    #The function takes the decrypted file, decrypts it and creates the non-encrypted file.
    chunksize = 64*1024
    output_file = filename[11:]

    with open(filename, 'rb') as infile:
        filsize = long(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filsize)


def get_key(password):
    #The function gets a new key
    hasher = SHA256.new(password)
    return hasher.digest()


def main():
    #The function parses all the options and uses them, it runs encryption and decryption according to the options.
    argparser = argparse.ArgumentParser()
    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-e", "--encrypt", help="Use the option to encrypt a file", action="store_true")
    group.add_argument("-d", "--decrypt", help="Use the option to decrypt a file", action="store_true")
    argparser.add_argument("-f", "--file", help="Insert the file you want to encrypt/decrypt.", type=str)
    argparser.add_argument("-p", "--password", help="Insert the password to to encrypt/decrypt the file.", type=str)
    args = argparser.parse_args()
    password = args.password
    filename = args.file

    if args.encrypt:
        encrypt(get_key(password), filename)
        print "The file " + filename + " was encrypted!"
        os.remove(filename)
    elif args.decrypt:
        decrypt(get_key(password), filename)
        print "The file " + filename + " was decrypted!"
        os.remove(filename)
    else:
        print "No option selected. Closing..."

if __name__ == '__main__':
    main()
