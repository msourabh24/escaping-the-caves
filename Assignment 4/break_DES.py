import os
from generate_text import *
from DES import *


def k6_sbox(sbox_in, inv_Feistel, exp_p, charac):
    test_keys = [[0 for col in range(64)] for row in range(8)]
    if charac == '0100000000001000000000000000000000000100000000000000000000000000':
        boxes = [2, 5, 6, 7, 8]
    else:
        boxes = [1, 2, 4, 5, 6]
    for i in range(len(inv_Feistel)):
        for j in boxes:
            box = j-1
            sbox_in_test = sbox_in[i][box*6:(box+1)*6]
            sbox_out_test = inv_Feistel[i][box*4:(box+1)*4]
            exp_p_test = exp_p[2*i][box*6:(box+1)*6]

            # Try out all possible key combinations for a S-Box to check whether it satisfies the differential
            for x in range(64):
                input_1 = "{:0>6b}".format(x)
                input_2 = xor(input_1, sbox_in_test)
                out_sbox_test = xor(s_box_out(input_1, j),
                                    s_box_out(input_2, j))
                # If it satisfies the differential, increase the frequency of the key in test_keys
                if out_sbox_test == sbox_out_test:
                    test_key = xor(input_1, exp_p_test)
                    test_keys[box][int(test_key, 2)] += 1
    # Find out the key with the maximum frequency for each S-Box possible and return the key in binary
    print("\nFor Characteristic (in binary): {}".format(charac))
    key = [''] * 8
    for i in boxes:
        avg_freq = sum(test_keys[i-1])//64
        max_freq = max(test_keys[i-1])
        key[i-1] = "{:0>6b}".format(test_keys[i-1].index(max_freq))
        print("Average Frequency of all possible keys for S-Box-{}: {}".format(i,avg_freq))
        print("Maximum Frequency for S-Box-{}: {} and its corresponding key: {}".format(i,max_freq, key[i-1]))
    return key


def break_des(number):

    crc_1 = '0100000000001000000000000000000000000100000000000000000000000000'
    crc_2 = '0000000000100000000000000000100000000000000000000000010000000000'
    input_txt = [[], []]
    cipher_txt = [[], []]

    # After generating plaintext-ciphertext pairs, don't poll the server again for multiple runs
    if (os.path.exists('plain_text.txt') and os.path.exists('cipher_text.txt')) == False:
        generate_text(number, crc_1)

    with open('plain_text.txt') as file:
        for i in file.readlines():
            input_txt[0] += [i[:-1]]
    with open('cipher_text.txt') as file:
        for i in file.readlines():
            cipher_txt[0] += [i[:-1]]

    if (os.path.exists('plain_text1.txt') and os.path.exists('cipher_text1.txt')) == False:
        generate_text(number, crc_2)

    with open('plain_text1.txt') as file:
        for i in file.readlines():
            input_txt[1] += [i[:-1]]
    with open('cipher_text1.txt') as file:
        for i in file.readlines():
            cipher_txt[1] += [i[:-1]]

    cipher_bin = [[], []]
    perm = [[], []]
    exp_p = [[], []]
    sbox_in = [[], []]
    Feistel_xor = [[], []]
    fout = [[], []]
    inv_Feistel = [[], []]

    for i in range(2):
        # For each ciphertext, computing the reverse permutations and expansions
        for j, x in enumerate(cipher_txt[i]):
            cipher_bin[i] += [str2bin(x)]
            perm[i] += [permute_64(cipher_bin[i][j], IP[4:] + IP[:4])]
            exp_p[i] += [expand(perm[i][j][0:32])]
        # for each ciphertext pair, computing the S-Box input XORs and output XORs
        for x in range(0, len(perm[i]), 2):
            sbox_in[i] += [xor(exp_p[i][x], exp_p[i][x+1])]
            Feistel_xor[i] += [xor(perm[i][x], perm[i][x+1])]

        for j, x in enumerate(Feistel_xor[i]):
            fout[i] += [x[32:]]
            inv_Feistel[i] += [permute(fout[i][j], REV_P)]

    bits_sbox = k6_sbox(
        sbox_in[0], inv_Feistel[0], exp_p[0], crc_1)
    bits_sbox_1 = k6_sbox(
        sbox_in[1], inv_Feistel[1], exp_p[1], crc_2)

    # Check whether the keys obtained are same for the common S-Boxes (2,5,6) from both the characteristics
    if bits_sbox[1] == bits_sbox_1[1] and bits_sbox_1[4] == bits_sbox[4] and bits_sbox[5] == bits_sbox_1[5]:
        partialkey = bits_sbox_1[0] + bits_sbox[1] + '??????' + bits_sbox_1[3] + \
            bits_sbox[4] + bits_sbox[5] + \
            bits_sbox[6] + bits_sbox[7]
        print("\nPartial Key extracted from S-Boxes (concatenated) (42 known bits out of 48): {}".format(partialkey))
    else:
        return False

    # Generate the 56-bit key using the 6-round keys mappings
    key64 = ['?'] * 64
    key56 = key64[:56]
    key_mapping = {}
    x = KEY_P1
    for i in range(1, 7):
        L = x[0:28]
        R = x[28:]
        L = L[SLT[i-1]:] + L[0:SLT[i-1]]
        R = R[SLT[i-1]:] + R[0:SLT[i-1]]
        x = L + R
        k = ['?']*48
        for j in range(0, 48):
            k[j] = x[KEY_P2[j]-1]
        key_mapping[i] = k

    # Using the 6th round key to map the partial key obtained from S-Boxes to the 64-bit key
    for j, c in enumerate(key_mapping[6]):
        key64[c-1] = partialkey[j]
    print("Partial Key mapped to 64-bit key: {}".format("".join(key64)))
    for j in range(0, 56):
        key56[j] = key64[KEY_P1[j]-1]
    print("Partial 56-bit Key made from 64-bit key using parity bit table: {}".format("".join(key56)))

    # Brute force the remaining 14-bits of the key
    for i in range(2**14):
        bits = "{:0>14b}".format(i)
        k = 0
        new_key = ""
        for c in key56:
            if c == '?':
                # generating new test key by substituting '?'
                new_key = new_key + bits[k]
                k = k+1
            else:
                new_key = new_key + c
        test_inp = str2bin(input_txt[0][0])
        test_out = str2bin(cipher_txt[0][0])
        # Test the key by checking on a known plaintext-ciphertext pair
        if des(test_inp, new_key, 1) == test_out:
            return new_key
    return False


# breaking DES using 2000 plaintext-ciphertext pairs corresponding to 1000 XORs for one characteristic
key = break_des(1000)
if key != False:
    print("Key extracted using Differential Cryptanalysis: {}".format(key))
    encrypted = 'nshkdsenpddldnljqsdefqffhoogrerm'
    decrypted = ''
    # decrypting 16 characters at a time using the obtained key
    decrypted_bin = des(
        str2bin(encrypted[:16]), key, 0) + des(str2bin(encrypted[16:]), key, 0)
    #
    for i in range(0, len(decrypted_bin), 8):
        decrypted += chr(int(decrypted_bin[i:i+8], 2))
    
    print("Password assuming the same mapping as in ciphertext: {}".format(bin2str(decrypted_bin)))
    print("Final Password (assuming ASCII): {}".format(decrypted))
    print("Final Password after removing the ending zeros: {}".format(decrypted[:10]))
else:
    print("Could not break DES, require more plaintext-ciphertext pairs")