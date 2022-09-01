import subprocess as sp


def str2int(s):
    '''Maps 2 character string to its corresponding integer value'''

    x = (ord(s[0]) - ord('f')) * 16 + ord(s[1]) - ord('f')
    return x


def int2str(x):
    '''Maps a integer (0-127) to its corresponding characters'''

    s = chr(ord('f') + x//16) + chr(ord('f') + x % 16)
    return s


def generate_text(plaintext):
    '''Generates ciphertext values for given plaintext from the ssh server'''

    plain_input = ['Cryptophile', 'Uuq53YDDJmsZsk',
                   '5', 'go', 'wave', 'dive', 'go', 'read']
    for p in plaintext:
        plain_input += [p, 'c']
    plain_input += ['back', 'exit']

    str_input = "\n".join(plain_input)
    str_input += "\n"

    # Obtain ciphertexts from the server
    p = sp.Popen(['sshpass', '-p', 'cs641a', 'ssh',
                 '-tt', 'students@172.27.26.188'], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    out = p.communicate(input=str_input.encode())[0].decode()

    # Write the output to a file and read for better formatting
    with open('output.txt', 'w') as file:
        file.write(out)
    with open('output.txt') as file:
        s = file.readlines()

    # Filter out the ciphertexts from the above output
    text = 'Slowly, a new text starts appearing on the screen. It reads ...\n'
    str_output = []
    for i, c in enumerate(s):
        if c == text:
            str_output += [s[i+1][2:-1]]

    # Return the list of ciphertexts obtained
    return str_output
