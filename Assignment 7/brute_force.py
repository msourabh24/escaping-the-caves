hash = [20, 10, 28, 62, 74, 125, 61, 84, 18, 125, 0, 37, 19, 125, 108, 4, 38, 92, 91, 112, 70, 84, 32, 86, 125, 87, 30, 13, 104, 3, 54, 101]
password = ''


def compute_e():
    e = [1]
    for k in range(1, hash[0]+1):
        tmp = 0
        for i in range(1, k+1):
            tmp += pow(-1, i-1) * e[k-i] * hash[i]
        tmp *= pow(k, 125, 127)
        tmp %= 127
        e.append(tmp)
    #print(e)
    return e


def update_hash(root):
    for k in range(len(hash)):
        tmp = hash[k]
        tmp -= pow(root, k, 127)
        tmp %= 127
        hash[k] = tmp
    #print(hash)


def is_root(val, e):
    poly = 0
    for k in range(hash[0]+1):
        poly += pow(-1, k) * e[k] * pow(val, hash[0] - k, 127)
        poly %= 127
    if poly == 0:
        return True
    return False


char = 'f'
while len(password) < 20:
    e = compute_e()
    if is_root(ord(char), e):
        password += char
        update_hash(ord(char))
    else:
        char = chr(ord(char) + 1)

print(f"Password : {password}")
