# This code requires the freebase function which can be located at my github repo:
# https://github.com/kingaling

import re


def ascii85_decode(x):
    att = ''
    for i in range(0, 256):
        att += chr(i) # att = all the things! charset containing all 256 chars

    ascii85 = ''
    for i in range(33, 118):
        ascii85 += chr(i) # ascii85 charset

    new_x = x.replace('\x00', '')
    new_x = new_x.replace('\x09', '')
    new_x = new_x.replace('\x0A', '')
    new_x = new_x.replace('\x0D', '')
    new_x = new_x.replace('\x20', '')
    new_x = new_x.replace('z', '!!!!!')

    end = re.search('~>', new_x).start()
    new_x = new_x[:end]

    lex = len(new_x) # length of x
    mox = lex % 5 # mod of x
    loops = lex / 5 # main loop count
    dec_str = ''

    if not mox == 0:
        padding = (5 - mox)
    else:
        padding = 0

    if padding > 0:
        loops += 1
        for i in range(0, padding):
            new_x += 'u'

    i = 0
    while i < (5 * loops):
        tmp = new_x[i:i+5]
        res = freebase(tmp, ascii85, att)
        if len(res) < 4:
            for j in range(0, 4 - len(res)):
                res = chr(0) + res
        i += 5
        dec_str += res

    if padding > 0 and len(dec_str) > 0:
        for i in range(0, padding):
            dec_str = dec_str[:-1]

    return dec_str


def ascii85_encode(x):
    att = ''
    for i in range(0, 256):
        att += chr(i) # att = all the things! charset containing all 256 chars

    ascii85 = ''
    for i in range(33, 118):
        ascii85 += chr(i) # ascii85 charset

    lex = len(x) # length of x
    mox = lex % 4 # mod of x
    loops = lex /4 # main loop count
    a85_str = ''
    for i in range(0, loops):
        idx = (i * 4) # setting index of x
        tmp = x[idx:idx+4]
        # freebase function converts from any base to any base
        # By passing source value (tmp), a source charset (att) and a destination charset (ascii85),
        # the following line sends a base 256 string of chars and gets back a base 85 string of chars.
        res = freebase(tmp, att, ascii85)

        # Encoding must return 5 bytes
        if len(res) < 5:
            for j in range(0, 5 - len(res)):
                res = '!' + res

        # Adobe replaces 5 !'s with a z
        if res == '!!!!!':
            res = 'z'
        a85_str += res

    # Now handle padding if the length of our chars wasn't divisible by 5
    tmp = x[loops * 4:loops * 4 + mox]
    for i in range(0, 4 - mox):
        tmp += chr(0)
    res = freebase(tmp, att, ascii85)
    res = res[:-(4 - mox)]
    if res == '!!!!!':
        res = 'z'
    a85_str += res + '~>'

    return a85_str


newdat = 'Put data here'

# Compress it
newdat = zlib.compress(newdat)

# ASCII85 encode it
newdat = ascii85_encode(newdat)

# ASCII85Decode it
newdat = ascii85_decode(newdat)

# Decompress it
newdat = zlib.decompress(newdat)

print newdat
