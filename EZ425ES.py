from ciphers425 import *
from cypari.gen import pari

def number_to_string(number):
    '''Represents the number in base 16 and converts 2-digits to ascii code character.
An '0' is placed in front of the hexstring if otherwise it would have an odd number
of digits.
'''
    hexstring = hex(number)
    ndigits = len(hexstring)-2
    if hexstring[-1]=='L': ndigits -= 1
    hexstring = hexstring[2:2+ndigits]
    if ndigits%2 is not 0:
        hexstring = '0'+hexstring
        ndigits += 1
    return ''.join( [chr(int(hexstring[x:x+2],16)) for x in range(0,ndigits,2)] )

n2s = number_to_string

def string_to_number(string):
    '''Each character in the string is replaced by it's ascii 2-hexdigit code.
The resulting long string is interrupted as an hexadeciaml number and returned as an integer.
'''
    return int(string.encode('hex'),16)

s2n = string_to_number

def hash425(string):
    return sum([ ord(char) for char in string ])%10000

def XOR425(key,string):
    '''The string is xor'd with the key in chunks of length of the key.
Extra spaces at the end are filled in with blank spaces'''
    if isinstance(key, int) or isinstance(key, long):
        k = key
        n = 16
    else:
        n = len(key)
        k = int(key.encode('hex'),16)
    extra = len(string) % n
    if extra is not 0: s = string + ' '*(n-extra)
    else: s = string
    encrypted = ''
    for x in range(0,len(s),n):
        encrypted += n2s(k^s2n(s[x:x+n]))
    return encrypted

##def XOR2(key,string):
##    if isinstance(key, int) or isinstance(key, long):
##        k = key
##        n = 16
##    else:
##        n = len(key)
##        k = int(key.encode('hex'),16)
##    extra = len(string) % n
##    if extra is not 0: s = string + ' '*(n-extra)
##    else: s = string
##    #print 'k = ', k
##    encrypted = ''
##    for x in range(0,len(s),n):
##        #print n, s[x:x+n]
##        enc_n = hex(k^( int(s[x:x+n].encode('hex'),16) ))[2:2*n+2]
##        #print enc_n
##        encrypted += ''.join( [ chr(int(enc_n[x:x+2],16)) for x in range(0,2*n,2) ] )
##    return encrypted

