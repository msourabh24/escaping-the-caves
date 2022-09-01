def decryption(cipher):
    # Square generated manually using 'CRYPTANALYSIS' and remaining squares filled with the alphabet sequentially
    square=[['C','R','Y','P','T'],
            ['A','N','L','S','I'],
            ['B','D','E','F','G'],
            ['H','K','M','O','Q'],
            ['U','V','W','X','Z']]
    
    # Converting cipher text to chunks of bigrams
    bigrams=[] 
    i=0
    while i < len(cipher):
        if i+1<len(cipher):
            bigrams+=[cipher[i]+cipher[i+1]]
            i+=2

    decrypted=''
    for p in bigrams:
        i1 = j1 = i2 = j2 = -1
        # Searching the bigram in the square
        for i in range(5):
            for j in range(5):
                if(square[i][j]==p[0]):
                    i1=i
                    j1=j
                if(square[i][j]==p[1]):
                    i2=i
                    j2=j
        # Decrypting the bigram using the square
        if i1 == i2: # Letters in same row
            decrypted += square[i1][(j1+4)%5] + square[i2][(j2+4)%5] # (x+4)%5 done to preserve cyclic order
        elif j1 == j2: # Letters in same column
            decrypted += square[(i1+4)%5][j1] + square[(i2+4)%5][j2]
        else:
            decrypted += square[i1][j2] + square[i2][j1]

    return decrypted

cipher = 'DF ULYP XO CQD LFWC RUBHEDY, CQDYG LN XDYL EGIYIG LMP CQDYF. LYFNH HXPZ CQF YNILXKPB "NDCB_AN_BBHCN" PQ FQ CQPKZBK. OLC PMC UNUG YMB IPYDIDCQ OXY CMB LDZP AULHDFY. CX OALG RMB FWGI PMX BNTIP ZLSWS LFWFE PQ ZCYGY KIBAT XMNKI PMBYD.'
cipher_txt = ''
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
space = ' '

# Removing spaces and punctuations from the cipher text
for i in cipher:
    if i in alphabet:
        cipher_txt += i

plain_text = decryption(cipher_txt)

# Inserting spaces and punctuation as observed in the cipher text at the correct places
j = 0
for i in cipher:
    if not i in alphabet:
        plain_text = plain_text[:j] + i + plain_text[j:]
    j += 1

print("Cipher Text: \n{}\n".format(cipher))
print("Plain Text (without removing the Xs and changing I to J based on context): \n{}\n".format(plain_text))