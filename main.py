#!/bin/bash/env python
# coding=UTF-8
# by Tarcisio marinho
# github.com/tarcisio-marinho

import argparse
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import os
import string
import random
import sys

'''
     use files to encrypt other file
'''

# argparse
parser = argparse.ArgumentParser(description='KeepSecret is a tool to cryptograph your files')
parser.add_argument('-e', '--encrypt', required = False, action = 'store_true',  help = 'File to be Encrypted/Decrypted')
parser.add_argument('-D', '--decrypt', required = False, action = 'store_true',  help = 'File to be Encrypted/Decrypted')
parser.add_argument('-f', '--file', type = str, required = False, metavar = '',  help = 'File to be Encrypted/Decrypted')
parser.add_argument('-d', '--directory', type = str, required = False, metavar = '', help = 'All files inside this Directory will be Encrypted/Decrypted')
parser.add_argument('-p', '--password', type = str, required = False, metavar = '', help = 'Password to Encrypt/Decrypt file')
args = parser.parse_args()

def instalation():
    pass


def error(er):
    sys.exit('Error: ' + er)

def generate_data(length):
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def shred(file_name,  passes):
    ld = os.path.getsize(file_name)
    fh = open(file_name,  "w")
    for _ in range(int(passes)):
        data = generate_data(ld)
        fh.write(data)
        fh.seek(0,  0)

    fh.close()
    os.remove(file_name)

def crypto(arq, password):
    if not os.path.isfile(arq):
        error('File does not exist.')
    else:
        try:
            with open(arq, 'rb') as f:
                pass
        except IOError as e:
            error('Error trying to open file: ' + str(e))

        with open(arq, 'rb') as in_file, open(arq + '.ks', 'wb') as out_file:
            encrypt(in_file, out_file, password)
        shred(arq, 1)

def decryptor(arq, password):
    if not os.path.isfile(arq):
        error('File does not exist.')
    else:
        try:
            with open(arq, 'rb') as f:
                pass
        except IOError as e:
            error('Error trying to open file: ' + str(e))

        if(os.path.splitext(arq)[1] == '.ks'):
            new = os.path.splitext(arq)[0]

        with open(arq, 'rb') as in_file, open(new, 'wb') as out_file:
            decrypt(in_file, out_file, password)
        shred(arq, 1)


def multiple_files(direc, password, mode):
    if(os.path.isdir(direc)):
        files_inside = []
        for path, folder, files in os.walk(direc):
            for arq in files:
                files_inside.append(os.path.join(path, arq))

        if(mode == 1):
            for files in files_inside:
                crypto(files, password)
        else:
            for files in files_inside:
                decryptor(files, password)

    else:
        error('Directory specified is not a directory at all.')

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

if __name__ == '__main__':
    if ((not args.file) and (args.directory)): # only dir
        if(args.password):
            if(args.encrypt and (not args.decrypt)):
                multiple_files(args.directory, args.password, 1) # encrypt
            elif(args.decrypt and (not args.encrypt)):
                multiple_files(args.directory, args.password, 2) # decrypt
            elif(args.decrypt and args.encrypt):
                error('Cannot encrypt and decrypt files at the same time.\nUse flag -h for help.')
            else:
                error('You need to specify wich operation: encrypt or decrypt\nUse flag -h for help.')
        else:
            error('You need to use a password.\nUse flag -h for help.')

    elif((args.file) and (not args.directory)): # only file
        if(args.password):
            if(args.encrypt and (not args.decrypt)):
                crypto(args.file, args.password)
            elif(args.decrypt and (not args.encrypt)):
                decryptor(args.file, args.password)
            elif(args.decrypt and args.encrypt):
                error('Cannot encrypt and decrypt file at the same time.\nUse flag -h for help.')
            else:
                error('You need to specify wich operation: encrypt or decrypt\nUse flag -h for help.')
        else:
            error('You need to use a password.\nUse flag -h for help.')

    elif((not args.file) and (not args.directory)): # neither
        error('You need to specify file or files inside a directory.')

    else: # both
        pass
