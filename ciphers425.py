try:
  from matmod import *
except: pass

A = 'YBRWY JFM N QCGYFR GIL SUZJX WJMFJ. NUJ VVL VBDM VS NUJ HRNAUGIEMIBI WBSMGFHGQS GJUFJX UNG. FTGRYCZJM GMYL TZSJLRI BVR U PMIVHY OJNJJYA F HVHERQ UAI U QNGR. OYFXY NQQNDM GTIX YBR SCPPYY-FZGJL NQF, VY QNX VVLARW. NUJ VVL VBDM YFOTMYQ FHQ QUHLBRI. IAJ XND USYYE OYFXY TWUOGYQ YBR SCPPYY, MCF KUGMYE YIBP BVR UFNXR FHQ XUVI, "DRXMR, YBBXY OTSF FLR RUXNHTKOA TZ LTO. GMYL YBVSE LTO QTHG PHBB NUJ XVRY VX QBWNU RIEJ NUFH GMY ANWXJF." WJMFJ AENHAJX NSX FFCQ, "IIAY QBWLL IUQ. N EATQ JMCPM CF BIEYB ZTLR. GOG NZ V YIBP NUJ XVRY, GMYL BIHQX FYIC IIVSA VY. MB KUE NPR HIYQYPYYQ $10 IIYQUEX."'
eng_freq = [('e', 12.7), ('t', 9.1), ('a', 8.2), ('o', 7.5), ('i', 7), ('n', 6.8), ('s', 6.3), ('h', 6.1), ('r', 6), ('d', 4.3), ('l', 4), ('u', 2.8), ('c', 2.8), ('w', 2.4), ('m', 2.4), ('f', 2.2), ('y', 2), ('g', 2), ('p', 1.9), ('b', 1.5), ('v', 1), ('k', 0.8), ('x', 0.2), ('j', 0.2), ('z', 0.1), ('q', 0.1)]

class Message(str):
  def __new__(cls, message, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      return str.__new__(cls,str(message))

  def __init__(self, message, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      if isinstance(message,Message):alphabet = message.alphabet
      self.alphabet = alphabet
      self.mod = len(alphabet)
      self.string = str(self)
      self.string_locations = {}

  def __repr__(self):
      return '*{}*'.format(self)

  def __getslice__(self,i,j):
      return Message(str.__getslice__(self,i,j),self.alphabet)

  def __getitem__(self,index):
      return Message(str.__getitem__(self,index),self.alphabet)

  def __eq__(self,other):
      try:
        return (self.alphabet == other.alphabet) and (str(self) == str(other))
      except AttributeError: return False
     
  def __add__(self,other):
      return(Message(str(self) + str(other),self.alphabet))
    
  def capitalize(self):
      return Message(str(self).capitalize(),self.alphabet)

  def center(self,width,fillchar=' '):
      return Message(str(self).center(width,fillchar),self.alphabet)

  def ljust(self,width,fillchar=' '):
      return Message(str(self).ljust(width,fillchar),self.alphabet)

  def expandtabs(self,tabsize = 8):
      return Message(str(self).expandtabs(tabsize),self.alphabet)

  def join(self):
      raise ValueError('messages cannot be joined')
  
  def lower(self):
      return Message(str(self).lower(),self.alphabet)

  def lstrip(self,chars = None):
      return Message(str(self).lstrip(chars),self.alphabet)

  def replace(self,old,new,count=None):
      if count == None: count = self.count(old)
      return Message(str(self).replace(old,new,count),self.alphabet)

  def swapcase(self):
      return Message(str(self).swapcase(),self.alphabet)

  def zfill(self,width):
      return Message(str(self).zfill(width),self.alphabet)

  def title(self):
      return Message(str(self).title(),self.alphabet)

  def upper(self):
      return Message(str(self).upper(),self.alphabet)

  def find_all(self,sub,start=0):
      count = 0
      F = 0
      while self.find(sub,start) != -1:
        count += 1
        start += len(sub)
      return count       

  def change_alphabet(self,alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      self.alphabet = alphabet
      self.mod = len(alphabet)
      return alphabet

  def good(self):
      """
     returns True if every character in the message is in the alphabet.  Otherwise
     returns a list of all characters not in the alphabet.
      """
      bad = []
      for x in self:
        if self.alphabet.rfind(x) == -1: bad = bad + [x]
      if len(bad) == 0: return True
      return bad

  def strip(self):
      """
  removes all characters not in alphabet.
      """
      strippedtext = ''
      for x in self:
          if self.alphabet.find(x)>-1:
            strippedtext=''.join([strippedtext,x])
      return Message(strippedtext,self.alphabet)

  def substitute(self,newalphabet='ZYXWVUTSRQPONMLKJIHGFEDCBA'):
      """
 Substitutes each alphabet character with corresponding letter in new alphabet.
 Default switches order of standard alphabet.
      """   
      alphabet = self.alphabet
      return Message( ''.join([newalphabet[alphabet.index(char)]
                        if char in alphabet else char
                        for char in self]),newalphabet)    

  def to_letters(self, numbers):
      """
      the nth character in return string is the numbers[n] letter in alphabet.
      """
      return ''.join(self.alphabet[numbers[i]] for i in range(len(numbers)))

  def to_integers(self):
      """
      Returns list of integer value for each character in text.
      """
      a=self.alphabet
      l = []
      for x in self:
          if x in a:
            l += [a.find(x) ]
          else:
            l += [x]
      return l
  
  def smoosh(self,n=5):
      """
      Strips the message of all characters not in the alphabet, inlcuding spaces, then
      separates the message into words of equal length = n
      """
      temp = self.strip()
      if n > 0:
        d,r = divmod(len(temp),n)
        sm = [ temp[n*i:n*(i+1)] for i in xrange(d) ]
        if r > 0: sm.append(temp[-r:])
        return Message(' '.join(sm))
      else:
        return temp


  def boxed(self,cols = 20):
      rows, remainder = divmod(len(self),cols)
      if remainder > 0: rows += 1
      return Message('\n'.join( [ '\t'.join( [char for char in row])
                                  for row in [self[cols*i:cols*(i+1)]
                                      for i in xrange(rows)] ] ), self.alphabet)
                     
  def unboxed(self):
      return self.replace('\t','').replace('\n','')


  def to_integerstring(self):
      """
      Returns string of 2-digit integer for each character in text.
      """
      return ''.join(
        ['%.2d'%z for z in self.to_integers ])

  def frequencies(self):
    alphabet = self.alphabet
    total = len(self)
    freq = [ ( x,round(float(self.count(x)) / total ,3) ) for x in alphabet]
    freq.sort(key=lambda x: x[0])
    return freq

  def shift_test(self,shifts=20):
    '''
Counts the number of coincidences in the text for each shift
    '''
    l = len(self)
    tests = [0]
    for shift in range(1,shifts):
      tests += [float(len([ x for x in range(l-shift) if self[x+shift]==self[x] ]))]
    return tests

  def groups(self,number):
    l = len(self)
    lg = l / number
    groups = []
    for n in range(number):
      groups += [ Message(''.join( [ self[x] for x in range(l) if x%number == n ] )) ]
    return groups

  def shift_correlation(self,group_freq,eng_freq):
    m = self.mod
    eng_freq = [('a', 8.2), ('b', 1.5), ('c', 2.8), ('d', 4.3), ('e', 12.7), ('f', 2.2), ('g', 2), ('h', 6.1), ('i', 7), ('j', 0.2), ('k', 0.8), ('l', 4), ('m', 2.4), ('n', 6.8), ('o', 7.5), ('p', 1.9), ('q', 0.1), ('r', 6), ('s', 6.3), ('t', 9.1), ('u', 2.8), ('v', 1), ('w', 2.4), ('x', 0.2), ('y', 2), ('z', 0.1)]
    return [ (j, sum([ group_freq[i][1]*eng_freq[(i+j)%m][1] for i in range(m) ]) ) for j in range(m) ]


class Cipher:

  def encrypt(self, plaintext):
      """
      Return encrypted version of text.
      """
      # Subclasses override this.
      ciphertext=''
      return ciphertext

  def decrypt(self, ciphertext):
      """
      Return decrypted version of text.
      """
      plaintext=''
      # Subclasses override this.
      return plaintext

  def crack(self, ciphertext):
      """
      Return decrypted version of textand the key.
      """
      plaintext=''
      key = ''
      # Subclasses override this.
      return key, plaintext

  
class AffineCipher(Cipher):

    def __init__(self, m = 1, b = 0):
        self.m, self.b = m , b
        if not ( isinstance(m, int) and isinstance(b, int) ):
            raise ValueError("m and b must be integers.")
              
    def change_key(self,m,b):
        if not ( isinstance(m, int) and isinstance(b, int) ):
            raise ValueError("m and b must be integers.")
        self.m, self.b = m , b
        return m,b
      
    def check_key(self,alphabet,m = None):
      if m == None: m = self.m
      if xgcd(m,len(alphabet))[0] != 1:
        return ( "m is not relatively prime to the length of the alphabet. "
        "m is not a good multiplicative key. "
        "You can encrypt but decryption is not reliable." )
      else:
        return ( "m is relatively prime to the length of the alphabet. "
        "m is a good multiplicative key." )

    def ciphertable(self, alphabet):
        cipheralphabet = self.encrypt(Message(alphabet,alphabet))
        print ''.join( ['{:2}'.format(x) for x in alphabet])
        print ''.join( ['{:2}'.format(x) for x in cipheralphabet])


    def affine(self, message, m , b):
        """
        transforms text by multiplying by m and then adding b
        """
        alphabet = message.alphabet
        mod = message.mod
        textlist=[alphabet[(m*alphabet.index(c)+b)% mod]
                  if c in alphabet else c
                  for c in message]
        return Message(''.join(textlist),alphabet)   
           
    def encrypt(self,message):
        """
        Encrypts by affine cipher, key x(m,b)
        """
        if not isinstance(message,Message): return 'bad Message'
        return self.affine(message,self.m,self.b)

    def decrypt(self,message = None):
        """
        Decrypts ciphertext that was encrypted with affine cipher, key (m,b)
        """
        if not isinstance(message,Message): raise ValueError('bad Message')
        gcd,minv,n = xgcd(self.m,message.mod)
        if gcd != 1: raise ValueError('m is not relatively prime to mod')
        return self.affine(message,minv,-minv*self.b)
          
class Caesar(AffineCipher):
    """
    Uses AffineCipher with m = 1.
    """
    def __init__(self, b=0):
        AffineCipher.__init__(self,1,b)

    def change_key(self,b):
        self.b = b
        return

    def crack1(self,message):
        """
        Prints out possible keys and decryptions of message with that key
        """
        alphabet = message.alphabet
        mod = message.mod
        for j in range(mod):
            newtext=''
            for i in range(len(message)):
                newtext += alphabet[(alphabet.index(message[i])-j)%mod]
            print 'key = {:2}: '.format(j), newtext

class SubstitutionCipher(Cipher):

    def __init__(self, alphabet, cipheralphabet):
        self.cipheralphabet = cipheralphabet
        self.alphabet = alphabet
        if len(alphabet) != len(cipheralphabet):
          raise ValueError('alphabets do not have same length')
 
    def encrypt(self,text):
        """
        returns encryted message with alphabet equal to cipher cipheralphabet
        """
        alphabet = self.alphabet
        cipheralphabet = self.cipheralphabet
        return Message(text,alphabet).substitute(cipheralphabet)

    def decrypt(self,message):
        """
        Decrypts ciphertext that was encrypted with affine cipher, key (m,b)
        """
        return message.substitute(self.alphabet)


class Vigenere(Cipher):
  
    def __init__(self,keyword = 'KEYWORD'):
      self.keyword = keyword.upper()
      self.keylength = len(self.keyword)

    def change_keyword(self,keyword):
      self.keyword = keyword.upper()
      self.keylength = len(self.keyword)
      return keyword
    
    def vig(self,message):
      alphabet = message.alphabet
      key = self.keyword
      kl = self.keylength
      L = len(message)
      textlist = list(message)
      count = 0
      newtext = ''
      while len(textlist):
        char = textlist.pop(0)     
        if char in alphabet:
          B = alphabet.index(key[count%kl])
          newtext += alphabet[(alphabet.index(char) + B) % message.mod]
          count+= 1
        else:
          newtext += char
      return Message(newtext,alphabet)

    def encrypt(self,message):
      if not isinstance(message,Message): return 'bad Message'
      return self.vig(message)

    def decrypt(self,message):
      """
decrypting will change the keyword to the decrypting keyword
use inverse_keyword to revert back and encrypt again
"""
      if not isinstance(message,Message): return 'bad Message'
      alphabet = message.alphabet
      mod = message.mod
      newkeyword = ''.join([alphabet[((mod - alphabet.index(letter)) % mod)]
                          for letter in self.keyword])
      self.change_keyword(newkeyword)
      return self.vig(message)
    
                                            
class HillCipher(Cipher):
  
    def __init__(self, matrix=Matmod([[1,2],[2,1]],26)):
        self.matrix = matrix
        self.dim = matrix.shape()[0]
     
    def blocks(self,message):
        alphabet = message.alphabet
        dim = self.dim
        ciphernumbers = message.to_integers()
        return [ [ciphernumbers[i] for i in range(dim*j,dim*(j+1))]
              for j in range(len(ciphernumbers)//dim)] |mod| message.mod

    def encrypt(self,message):
        alphabet = message.alphabet
        D = self.blocks(message) * self.matrix
        nrows,columns = D.shape()
#        print nrows,columns,D
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet) 

    def decrypt(self,message):
        """
        Created by Nathan Lavy. Spring 2013.
        This decrypts the given string.  The string must be of length divisible by the dimension of the matrix.
        If the string is not divisible by the dimension of the matrix, then the extra characters will be truncated.
        """
        
        ## This cannot work for strings of length not divisible by the dimension of the matrix.
        ## This is because all of the characters in then encrypted string
        ##    provide information that is used to decrypt the string.
        ## example:
        ##    Suppose we have: m = [ 00, 00, 01 ]
        ##                         [ 00, 01, 00 ]
        ##                         [ 01, 00, 00 ]  mod 26
        ##    Suppose further that there is only one character that is unknown.
        ##    The plaintext would look like: '?xx', where '?' can be any letter (the pad is 'x', which integer value is 23)
        ##    The encrypted string would look like: [ 23, 23, $ ], where $ is the encrypted number for ?
        ##    The equations that generated this is:
        ##        ? * 0 + 23 * 0 + 23 * 1 = 23 mod 26
        ##        ? * 0 + 23 * 1 + 23 * 0 = 23 mod 26
        ##        ? * 1 + 23 * 0 + 23 * 0 =  $ mod 26
        ##    If the encrypted string is truncated, then the encrypted string would be: [ 23 ]
        ##    If we would try to decrpyt this with a system of equations, they would look like:
        ##        a * 0 + 23 * 0 + 23 * 1 = 23 mod 26  --->   23 = 23 mod 26
        ##        a * 0 + 23 * 1 + 23 * 0 =  b mod 26  --->    b = 23 mod 26
        ##        a * 1 + 23 * 0 + 23 * 0 =  c mod 26  --->    a =  c mod 26
        ##    From this, a and c can be anything (as long as they are equivalent mod 26), which means we cannot decrypt it.
        ##    Because I was able to find a situation that needed all of the characters (numbers) in the encrypted
        ##        string (made with the pad) to be able to decrypt, the pad must be kept in the encrypted string.

        alphabet = message.alphabet
        matrix_inverse = self.matrix ^ -1
        D = self.blocks(message) * matrix_inverse
        nrows,columns = D.shape()
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet)

    def unblock(self,D,alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        nrows,columns = D.shape()
        return Message(''.join( [ ''.join( [ alphabet[x.lift()] for x in D[j] ] )
                          for j in range(nrows) ] ),alphabet)
        

class RSA_prot(Cipher):
    ''' N is the product of two large primes which are not known for encrypting,
but must be known to decrypt.  e is a number relative prime to (p-1)*(q-1)
    '''
    def __init__(self,N,e,p=1,q=1):
       self.N, self.p, self.q, self.e = N,p,q,e
       if p!= 1:
         self.N = p*q

    def encrypt(self,message):
        ''' message is an integer.
        '''
        m = Matmod(message,self.N)
        return (m^self.e).lift()

    def decrypt(self,message):
        ''' message is an integer.
        '''
        dmod = (self.p-1)*(self.q-1)
        if dmod == 0:
          return 'can\'t decrypt'
        else:
          m = Matmod(message,self.N)
          d = (Matmod(self.e,dmod))^-1
          return (m^(d.lift())).lift()
        
 
def cards():
    alphabet = 'A234567890JQK'
    return Message('JA' + 'C'.join(alphabet) + 'C' +
                   'D'.join(alphabet) + 'D' + 'H'.join(alphabet) + 'H' +
                   'S'.join(alphabet) +'S' + 'JB', alphabet = 'A234567890JQK')

def xgcd(A,B):
    """
    Finds g=gcd(A,B) and solves the equation A*n+B*m=gcd(A,B)
    """
    a, b = A, B
    n1, m1, n, m = 0, 1, 1, 0
    if B == 0:
      return A, 1, 0
    r = b
    while r > 0:
        g = r
        q,r = divmod(a,b)
        n1,m1,n,m = n-q*n1,m-q*m1,n1,m1
        a, b = b, r       
        #A*n1+B*m1=r, last time will be r = 0, so A*n+B*m=g 
    return g,n,m


      

     

#if __name__ == '__main__':
    
