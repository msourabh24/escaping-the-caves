a = [429,
     1973,
     7596]

b = [431955503618234519808008749742,
     176325509039323911968355873643,
     98486971404861992487294722613]

P = 455470209427676832372575348833

def gcd_coeff(a, b, x, y):
    if b == 0:
        x = 1
        y = 0
        return [a, x, y]

    x1 = 0
    y1 = 0
    [d, x1, y1] = gcd_coeff(b, a%b, x1, y1) #calculating GCD using Euler's Algorithm
    x = y1
    y = x1 - y1*(a//b)
    return [d, x, y]

x = 0
y = 0
[gcd, x, y] = gcd_coeff(a[1] - a[0], a[2] - a[0], x, y)
# print(x, y)

b_inv = [pow(i , -1, P) for i in b]

diff1 = pow(b[1]*b_inv[0], -x, P)
diff1 = pow(diff1, -1, P)
diff2 = pow(b[2]*b_inv[0], y, P)

g = (diff1 * diff2) % P

password = (b[0] * pow(g, -1*a[0], P)) % P
print("g is {} and Password is {}".format(g, password))

