from generate_text import *

encrypted_password = 'lhltfpjnfnfmgmmpljllgohqlpkokpmk'


def break_AES(encr_pass):
    '''Breaks through the encryption'''
    decr_pass = ""
    for r in range(2):
        decr_half = ""
        for b in range(0, 16, 2):
            idx = 16 * r + b
            plaintext = []

            # Generates all possible bytes from [ff, mu] (128 possible)
            # to check whether it matches the encrypted text
            for i in range(128):
                plaintext += [decr_half + int2str(i)]
            ciphertext = generate_text(plaintext)

            # Checks all the ciphertexts for the correct mapping with
            # the encrypted password
            for i in range(128):
                if encr_pass[idx:idx+2] == ciphertext[i][b:b+2]:
                    decr_half += int2str(i)
                    print("{} -> {}".format(encr_pass[idx:idx+2], int2str(i)))
        decr_pass += decr_half
        print("\nPT{}: {}\n".format(r+1, decr_half))
    # Return the entire 32 character long decrypted password
    return decr_pass


print("Given below is the mapping for the given encrypted password: {}".format(
    encrypted_password))
print("Ciphertext -> Plaintext")

decrypted_password = break_AES(encrypted_password)
print("Decrypted Password: {}".format(decrypted_password))

# Convert the decrypted password to ASCII
actual_password = ""
for i in range(0, 32, 2):
    actual_password += chr(str2int(decrypted_password[i:i+2]))
print("\nActual Password after converting to ASCII: {}".format(actual_password))

# Remove padding from the password
password = actual_password[:-6]
print("\nPassword after removing the padding: {}".format(password))
