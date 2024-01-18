# hash function hash(s) = s[0] + s[1]*p + s[2]*p^2 + ... + s[n-1]*p^(n-1) mod m
# where s is a string, p is a prime number, m is the size of the hash table

# hash(l, r) = for i in range(l, r+1): hash += s[i]*p^(i-l) mod m
# here is l is removed from i, so we can take l common from the power of p
# now multiply by p^l on both sides
# hash(l, r) * p^l = for i in range(l, r+1): hash += s[i]*p^(i) mod m
                #  = hash(0, r) - hash(0, l-1) mod m
#         hash(l, r) = (hash(0, r) - hash(0, l-1)) * p^(-l) mod m (p^(-l) is the inverse of p^l mod m)


from typing import List


def power(x, y, m):

    result = 1
    while y:
        if y & 1:
            result = (result*x)%m
        y >>= 1
        x = (x*x)%m

    return result


inv = [0] * 1000000
def stringhashing(s: str) -> List:
    p = 31
    m = int(1e9+7)
    inv[0] = 1
    hsh = [(ord(s[0])-ord('a')+1) % m]
    ppow = 1
    for i in range(1, len(s)):
        ppow = (ppow * p) % m
        cur_hash = ((ord(s[i])-ord('a')+1) * ppow) % m
        inv[i] = power(ppow, m-2, m)

        hsh.append((hsh[-1] + cur_hash) % m)

    return hsh

def get_substring_hash(hsh: List, l: int, r: int) -> int:
    res = hsh[r]
    m = int(1e9+7)
    if l > 0:
        res -= hsh[l-1]
        res += m
    res = (res * inv[l])%m

    return res % m

hashh = stringhashing("helloworld")
print(hashh)
print(get_substring_hash(hashh, 5, 9))
hash1 = stringhashing("world")
print(hash1[-1])
