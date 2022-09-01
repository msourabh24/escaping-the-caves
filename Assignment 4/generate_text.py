from DES import *
import random
import subprocess as sp


def str2bin(s):
    '''Map 'defghijklmnopqrs' to binary'''
    out = ""
    for i in s:
        out = out + "{:0>4b}".format(ord(i) - ord('d'))
    return out


def bin2str(s):
    '''Reverse of str2bin'''
    out = ""
    for i in range(0, len(s), 4):
        out = out + chr(ord('d') + int(s[i:i+4], 2))
    return out


def generate_text(number, characteristic):
    '''Generate plaintext-ciphertext pairs for differential cryptanalysis'''

    REP = [[40, 8, 48, 16, 56, 24, 64, 32],
           [39, 7, 47, 15, 55, 23, 63, 31],
           [38, 6, 46, 14, 54, 22, 62, 30],
           [37, 5, 45, 13, 53, 21, 61, 29],
           [36, 4, 44, 12, 52, 20, 60, 28],
           [35, 3, 43, 11, 51, 19, 59, 27],
           [34, 2, 42, 10, 50, 18, 58, 26],
           [33, 1, 41, 9, 49, 17, 57, 25]]
    # Apply reverse final permutation
    rev_permutation = permute_64(characteristic, REP)
    # only_inputs = stores only the input plaintexts
    # plain_input = stores the payload to be given to sshpass
    plain_input = ['Cryptophile', 'Uuq53YDDJmsZsk', '4', 'read']
    only_inputs = []
    for x in range(number):
        plain_text = ""
        for j in range(16):
            plain_text += "".join(random.choices(
                [c for c in 'defghijklmnopqrs']))

        plain_bin = str2bin(plain_text)
        plain_bin2 = xor(plain_bin, rev_permutation)

        plain_input += [bin2str(plain_bin), 'c', bin2str(plain_bin2), 'c']
        only_inputs += [bin2str(plain_bin), bin2str(plain_bin2)]
    plain_input += ['back', 'exit']
    # write the contents of plain_input to input.txt for logging
    with open('input.txt', 'w') as file:
        for s in plain_input:
            file.write(s)
            file.write("\n")
    # read the contents of input.txt
    with open('input.txt') as file:
        str_input = file.readlines()
    str_input = "".join(str_input)

    # pass str_input to the sshpass which opens the server to generate ciphertext pairs
    p = sp.Popen(['sshpass', '-p', 'cs641a', 'ssh', '-tt',
                 'students@172.27.26.188'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    out = p.communicate(input=str_input.encode())[0].decode()
    # write the output to output.txt for logging and further cleaning
    with open('output.txt', 'w') as file:
        file.write(out)
    with open('output.txt') as file:
        s = file.readlines()
    
    # filter out the ciphertexts from the output of sshpass
    text = 'Slowly, a new text starts appearing on the screen. It reads ...\n'
    str_output = []
    for i, c in enumerate(s):
        if c == text:
            str_output += [s[i+1][2:-1]]
    # write the ciphertexts generated for specific characteristics to different files
    if characteristic == "0100000000001000000000000000000000000100000000000000000000000000":
        file_in = open("plain_text.txt", "w")
        file_out = open("cipher_text.txt", "w")
    elif characteristic == "0000000000100000000000000000100000000000000000000000010000000000":
        file_in = open("plain_text1.txt", "w")
        file_out = open("cipher_text1.txt", "w")

    for i in only_inputs:
        file_in.write(i)
        file_in.write("\n")
    file_in.close()

    for i in str_output:
        file_out.write(i)
        file_out.write("\n")
    file_out.close()
