# DES implementation for 6 rounds

IP = [[58, 50, 42, 34, 26, 18, 10, 2],
      [60, 52, 44, 36, 28, 20, 12, 4],
      [62, 54, 46, 38, 30, 22, 14, 6],
      [64, 56, 48, 40, 32, 24, 16, 8],
      [57, 49, 41, 33, 25, 17, 9, 1],
      [59, 51, 43, 35, 27, 19, 11, 3],
      [61, 53, 45, 37, 29, 21, 13, 5],
      [63, 55, 47, 39, 31, 23, 15, 7]]

FP = [[8, 40, 16, 48, 24, 56, 32, 64],
      [7, 39, 15, 47, 23, 55, 31, 63],
      [6, 38, 14, 46, 22, 54, 30, 62],
      [5, 37, 13, 45, 21, 53, 29, 61],
      [4, 36, 12, 44, 20, 52, 28, 60],
      [3, 35, 11, 43, 19, 51, 27, 59],
      [2, 34, 10, 42, 18, 50, 26, 58],
      [1, 33, 9,  41, 17, 49, 25, 57]]


E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

REV_P = [9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10, 1,
         8, 14, 25, 3, 4, 29, 11, 19, 32, 12, 22, 7, 5, 27, 15, 21]

S_BOX = {
    1: [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    2: [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    3: [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    4: [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    5: [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    6: [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    7: [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    8: [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
}

KEY_P1 = [57, 49, 41, 33, 25, 17, 9,
          1,  58, 50, 42, 34, 26, 18,
          10, 2,  59, 51, 43, 35, 27,
          19, 11, 3, 60, 52, 44, 36,
          63, 55, 47, 39, 31, 23, 15,
          7, 62, 54, 46, 38, 30, 22,
          14, 6, 61, 53, 45, 37, 29,
          21, 13, 5, 28, 20, 12, 4]

SLT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

KEY_P2 = [14, 17, 11, 24, 1, 5,
          3, 28, 15, 6, 21, 10,
          23, 19, 12, 4,  26, 8,
          16, 7, 27, 20, 13, 2,
          41, 52, 31, 37, 47, 55,
          30, 40, 51, 45, 33, 48,
          44, 49, 39, 56, 34, 53,
          46, 42, 50, 36, 29, 32]


def generate_keys(key, en):
    '''Generate keys for each round of DES (6 rounds)'''
    keys = {}
    x = key
    for i in range(1, 7):
        L = x[0:28]
        R = x[28:]
        L = L[SLT[i-1]:] + L[0:SLT[i-1]]
        R = R[SLT[i-1]:] + R[0:SLT[i-1]]
        x = L + R
        k = ""
        for j in range(0, 48):
            k += x[KEY_P2[j]-1]
        if en == 1:
            keys[i] = k
        else:
            keys[7-i] = k
    return keys


def s_box_out(s, sbox):
    '''Returns the 4-bit output of sbox'th S-Box given a 6-bit input'''
    out = ""
    c = int(s[1:5], 2)
    r = int(s[0]+s[5], 2)
    out = out + "{:0>4b}".format(S_BOX[sbox][r][c])
    return out


def xor(x, y):
    '''Returns the XOR of x and y'''
    out = ""
    for i in range(len(x)):
        out = out + str(int(x[i]) ^ int(y[i]))
    return out


def expand(s):
    '''Returns a 48-bit string expanded from 32-bit input using E matrix'''
    out = ""
    for i in range(48):
        out = out + s[E[i]-1]
    return out


def permute_64(s, perm):
    '''Permute a given string s based on the permutation matrix perm'''
    t = ""
    for i in range(len(s)):
        t = t + s[perm[i//8][i % 8] - 1]
    return t


def permute(s, perm):
    '''Permute a given string s based on the permutation array perm'''
    t = ""
    for i in range(len(s)):
        t = t + s[perm[i] - 1]
    return t


def des(s, key, en):
    '''Encrypt (en=1) or decrypt(en=0) upto round 6 using key'''
    # Apply initial permutation to the 64-Bit input
    s = permute_64(s, IP)
    keys = generate_keys(key, en)

    for i in range(1, 7):
        # Split the 64-Bit input to left and right half
        L = s[0:32]
        R = s[32:]
        # Expand the right half using the expansion matrix
        exp_R = expand(R)
        # XOR expanded R with the round key
        R_key = xor(exp_R, keys[i])
        # Generate the S-Box output for this round
        SBox_out = ""
        for j in range(0, 48, 6):
            SBox_out = SBox_out + s_box_out(R_key[j:j+6], j//6 + 1)
        # Apply permutation to the 32-bit output of the S-Box
        p = permute(SBox_out, P)
        # Combine the new L (old R) and new R (permutation XORed with L)
        s = R + xor(p, L)
    # Apply final permutation after 6 rounds
    s = permute_64(s, FP)
    return s