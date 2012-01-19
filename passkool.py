#
# PassKool v0.2 - A deterministic 'intelligible' generator
# Copyright (C) 2004-2005 - Kevin Drapel (kevin.drapel@epfl.ch)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# $Id$

"""PassKool v0.2 - A deterministic 'intelligible' password generator
Mon Apr 11 18:25:04 CEST 2005
Copyright (C) 2004-2005 - Kevin Drapel (kevin.drapel@epfl.ch)

Usage: python passkool.py "account" "passphrase" [OPTIONS]

Options : 
  -l,  --length            length of the generated password (must be above 4)
  -r,  --random               use "pretty random" mode instead of Markov chains
  -s,  --special           force special characters (25% of final password)
  -n,  --numbers           add some digits into the password (25% of password)
  -c,  --mixcase           mix lower and upper case characters
  -h,  --help              print help

The "account" is  for  example  your username  or  some URL. The "passphrase" is
a sentence that  you can  easily remember but  quite  difficult  to guess for an 
attacker, the minimum passphrase length is 16 characters. 
 
Examples :
    
python passkool.py "root" "top secret phrase"
---> Generated password : quencatithro

python passkool.py "root" "top secret phrase" -c -n 
---> Generated password : Quenc7t257ro

python passkool.py "root" "top secret phrase" -l 16
---> Generated password : ontimenttimewhen

python passkool.py "root" "top secret phrase" -l 16 --special
---> Generated password : o)*ime!t$i!ewhen

python passkool.py "root" "top secret phrase" -l 16 --random
---> Generated password : dG3nJc#g$;Lk^#N2

By default, the length  is  12 and  the "pretty random"  mode  is  disabled. The 
random  mode generates  deterministic passwords with  high  entropy. The default
mode uses Markov chains to produce more or less English passwords, they are less
secure  than random  passwords  but still good for most  purposes. Changing  one
character in the passphrase or the  account will completely modify the generated
password.  The one-way  conversion  is performed  in a  deterministic  way,  the 
generated  password will  be the same as long  as you type  the same  arguments. 
Some  special  characters are added  to improve  security against  a brute-force 
attack. At  least 25%  of the  password is  composed of  special or  punctuation 
characters if you enable the '-s' switch. With '-n' you will add some digits."""

__author__ = "Kevin Drapel"
__version__ = "$Revision$"
__date__ = "$Date$"
__copyright__ = "Copyright (c) 2004 - Kevin Drapel"
__license__ = "GPL"


import string,sys
import copy
import sha, random, getopt
##from sets import Set

#############################################################################

# print usage if wrong or no arguments have been given in command line
def usage():
    print __doc__
    sys.exit()
    
# turn a passphrase into a SHA digest
def digestPhraseSHA(secretPhrase):
    hashFunc = sha.new()
    hashFunc.update(secretPhrase)
    return hashFunc.hexdigest()
    
 
def randomShaInt(maxValue):
    global shaSeed 
    shaSeed = digestPhraseSHA(shaSeed)
    return int(shaSeed,16) % maxValue
    
# main function
def main(argv):
    global shaSeed 
    shaSeed = 0
    # the "pretty random" mode is not used by default
    useRandomNotMarkov = False
    # special chars is disabled by default
    useSpecialChars = False
    # numbers are disabled by default
    useNumbers = False
    # swap case is disabled by default
    useSwap = False
    
    if len(argv) < 2:
        usage()
    else: 
        # parse arguments
        try:
            optList, args = getopt.getopt(sys.argv[3:], 'hl:rscn', ["help", "length=", "random", "special", "mixcase", "numbers"])
        except getopt.GetoptError:
            usage()
        
        # default password length
        passwordLength = 12
        
        # look for options
        for opt in optList:
            if opt[0] in ("-l", "--length"):
                passwordLength = int(opt[1])
            if opt[0] in ("-r", "--random"):
                useRandomNotMarkov = True
            if opt[0] in ("-n", "--numbers"):
                useNumbers = True
            if opt[0] in ("-c", "--mixcase"):
                useSwap = True
            if opt[0] in ("-s", "--special"):
                useSpecialChars = True
            if opt[0] in ("-h", "--help"):
                usage()

        # check parameters
        if len(argv[1])<16:
            print "\n>>>> ERROR : Your passphrase is too short, use at least 16 characters"
            sys.exit()
        
        if passwordLength<4:
            print "\n>>>> ERROR : Your password needs at least 4 characters"
            sys.exit()
            
        # append the two strings together, this will be used as a seed
        # for the stochastic process
        seed = argv[0]+argv[1]+hex(int(passwordLength))
        result = digestPhraseSHA(seed)
        
        # generate the RNG seed according to password length and
        # passphrase
        for i in range(0,passwordLength):
            result = digestPhraseSHA(result)
        
        shaSeed = result
        
        #########################random.seed(result)
        
        # the user can use the special "pretty random" mode
        # the password will be more secure intelligible
        # this charset contains most characters except back-tick and
        # backslash which are somehow inconvenient to type
        if useRandomNotMarkov:
            randomCharset = []
            password = ""
            
            for i in range(33,91):
                randomCharset.append(chr(i))
            for i in range(93,95):
                randomCharset.append(chr(i))
            for i in range(97,122):
                randomCharset.append(chr(i))
            for i in range(0,passwordLength): 
                password += randomCharset[randomShaInt(len(randomCharset)-1)]
            print "\n---> Generated password : "  + ''.join(password)
            sys.exit()
        
        
        # read the text used for generating the english
        # frequency tables 
        wholeText = ""
        f = open("markov.dat")
        lines = f.readlines()
        for line in lines:
            wholeText += line
            line = line[:-1]
        f.close()
        
        # remove line breaks and turns everything into
        # lowercase
        wholeText = wholeText.lower()
        
        cleanText = ""
        # remove non-letters
        for i in range(0,len(wholeText)-1):
            if wholeText[i] in string.ascii_lowercase:
                cleanText += wholeText[i]
        
        wholeText = cleanText 
        
        # create a table of frequency (dictionnary) using
        # a 4-uple of characters as key
        freqTable = {}
        for i in range(0,(len(wholeText)-3-1),1):
            key = wholeText[i]+wholeText[i+1]+wholeText[i+2]+wholeText[i+3]
            if freqTable.has_key(key):
                freqTable[key]=freqTable[key]+1
            else:
                freqTable[key]=1
        
        # THE MARKOV GENERATOR
        lgTable = len(freqTable.keys())
        allKeys = freqTable.keys()
        
        r = randomShaInt(lgTable-1)
        currentTrig = allKeys[r]
        
        # start with a random trigram, this trigram is added to
        # the password but will be trimmed at the end, this will slighty
        # improve the security
        currentText = []
        currentText += currentTrig[0:3]

        # add characters until the password is done
        for i in range(0,passwordLength,1): 
            matching = []
            
            # find all matching trigrams
            for n in range(0,lgTable,1):
                if currentTrig[0:3]==allKeys[n][0:3]:
                    matching.append(copy.deepcopy([allKeys[n][3],freqTable[allKeys[n]]]))
        
            # roulette-wheel selection
            total = 0
            for n in matching:
                total+=n[1]
            for n in matching:
                n[1]/=float(total)
            
            total = 0
            rnd = randomShaInt(12345678)/12345678.0
            for m in matching:
                total += m[1]
                if rnd<=total: 
                    currentText += m[0]    
                    break
                    
            # a character has been added, make a new trigram
            # for next character
            l = len(currentText)
            currentTrig = currentText[l-3]+currentText[l-2]+currentText[l-1]
            
            # change trigams every 10 characters to avoid long runs
            # without much randomness
        
        # remove the first 3 letters
        finalPassword = currentText[3:]
            
        # THE ENTROPY-MAKER 
        
        # create a special charset
        asciiRangeSpecial = []
        if useSpecialChars == True:
            for i in range(33,46):
                asciiRangeSpecial.append(chr(i))
        
        if useNumbers == True:
            for i in range(48,57):
                asciiRangeSpecial.append(chr(i))
            
        # change some cases
        if useSwap == True:
            for i in range(0,passwordLength/2):
                k = randomShaInt(len(finalPassword)-1)
                finalPassword[k]=finalPassword[k].swapcase()
                    
        # add some special chars until there are N of them
        # (at least 25% of the chars must be special)

        while True and len(asciiRangeSpecial)!=0 :
            total=0
            for i in range(0,len(finalPassword)):
                if finalPassword[i] in asciiRangeSpecial:
                    total+=1
            # replace some chars by special chars
            if total>passwordLength/4:
                break
            else: 
                k = randomShaInt(len(finalPassword)-1)
                finalPassword[k]=asciiRangeSpecial[randomShaInt(len(asciiRangeSpecial)-1)]
                
        # print final result
        print "\n---> Generated password : "  + ''.join(finalPassword)
        

        
#############################################################################

if __name__ == "__main__":
    main(sys.argv[1:])
    
    
