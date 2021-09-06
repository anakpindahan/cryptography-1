import re
from collections import deque

def letterToRank(letter):
    return(ord(letter.lower()) - ord('a'))

def rankToLetter(rank):
    return(chr(rank + ord('a')))

def fitKey(key, textLength):
    remainder = textLength % len(key)
    repeats = textLength // len(key)
    return(repeats * key + key[:remainder])

def stripNonLetterChars(anyText):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('', anyText)

def makePlayfairKey(anyText):
    # Discard all non-alphabetic character and J
    anyText = anyText.upper()
    regex = re.compile('[^A-IK-Z]')
    anyText = regex.sub('', anyText)

    # Remove double letter
    return(''.join(sorted(set(anyText), key=anyText.index)))


def constructPlayfairMatrix(key):
    keyText = makePlayfairKey(key)
    playfairMatrix = [["" for _ in range(5)] for _ in range(5)]
    for i in range(len(keyText)):
        row = i // 5
        column = i  % 5
        playfairMatrix[row][column] = keyText[i]
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    regexStatement = '['
    for letter in keyText:
        regexStatement += letter
    regexStatement += ']'
    regex = re.compile(regexStatement)
    alphabet = regex.sub('', alphabet)

    for j in range(len(alphabet)):
        row = (j + len(keyText)) // 5
        column = (j + len(keyText)) % 5
        playfairMatrix[row][column] = alphabet[j]

    return playfairMatrix

def makePlayfairDict(playfairMatrix):
    playfairDict = {}
    for i in range(5):
        for j in range(5):
            playfairDict[playfairMatrix[i][j]] = [i, j]
    return playfairDict

def encodeLettersPlayfair(bigram, playfairDict, playfairMatrix):
    position1 = playfairDict[bigram[0]]
    position2 = playfairDict[bigram[1]]

    cipherBigram = []
    if(position1[0] == position2[0]):
        cipherBigram = [
            playfairMatrix[position1[0]][(position1[1] + 1) % 5],
            playfairMatrix[position2[0]][(position2[1] + 1) % 5]
        ]
    elif(position1[1] == position2[1]):
        cipherBigram = [
            playfairMatrix[(position1[0] + 1) % 5][position1[1]],
            playfairMatrix[(position2[0] + 1) % 5][position2[1]]
        ]
    else:
        cipherBigram = [
            playfairMatrix[position1[0]][position2[1]],
            playfairMatrix[position2[0]][position1[1]]
        ]
    return cipherBigram

def decodeLettersPlayfair(bigram, playfairDict, playfairMatrix):
    position1 = playfairDict[bigram[0]]
    position2 = playfairDict[bigram[1]]

    decipherBigram = []
    if(position1[0] == position2[0]):
        decipherBigram = [
            playfairMatrix[position1[0]][(position1[1] - 1) % 5],
            playfairMatrix[position2[0]][(position2[1] - 1) % 5]
        ]
    elif(position1[1] == position2[1]):
        decipherBigram = [
            playfairMatrix[(position1[0] - 1) % 5][position1[1]],
            playfairMatrix[(position2[0] - 1) % 5][position2[1]]
        ]
    else:
        decipherBigram = [
            playfairMatrix[position1[0]][position2[1]],
            playfairMatrix[position2[0]][position1[1]]
        ]
    return decipherBigram

def makePlayfairPlaintext(anyText):
    anyText = stripNonLetterChars(anyText.upper())
    letterList = [letter for letter in anyText]
    pairList = []
    letterListLength = len(letterList)
    while(letterListLength > 0):
        if(len(letterList) == 1 and letterList[0] != 'X'):
            pairList.append([letterList[0], 'X'])
            del letterList[0]
            letterListLength -= 1
        elif(len(letterList) == 1 and letterList[0] == 'X'):
            pairList.append(['X', 'Z'])
            del letterList[0]
            letterListLength -= 1
        elif(letterList[0] == letterList[1]):
            pairList.append([letterList[0], 'X'])
            del letterList[0]
            letterListLength -= 1
        else:
            pairList.append([letterList[0], letterList[1]])
            del letterList[0]
            del letterList[0]
            letterListLength -= 2
    return pairList

def makePlayfairCiphertext(anyText):
    anyText = stripNonLetterChars(anyText.upper())
    letterList = [letter for letter in anyText]
    pairList = []
    for i in range(len(letterList)//2):
        pairList.append([letterList[2*i], letterList[2*i + 1]])
    return pairList

def inverseModulo(x, m):
    # Using extended euclidean algorithm
    a = 1
    b = 0
    n = m
    
    while(x > 1):

        q = x // m
        tempM = m

        m = x % m
        x = tempM
        tempM = b

        b = a - q * b
        a = tempM

    return a % n
    
def vigenereEncrypt(plainText, key):
    plainText = stripNonLetterChars(plainText)
    fittedKey = fitKey(stripNonLetterChars(key), len(plainText))
    vigenereEncrypted = ''
    for i in range(len(plainText)):
        vigenereEncrypted += rankToLetter((letterToRank(plainText[i])  + letterToRank(fittedKey[i])) % 26)
    return vigenereEncrypted.upper()

def vigenereDecrypt(cipherText, key):
    cipherText.lower()
    fittedKey = fitKey(stripNonLetterChars(key), len(cipherText))
    vigenereDecrypted = ''
    for i in range(len(cipherText)):
        vigenereDecrypted += rankToLetter((letterToRank(cipherText[i])  - letterToRank(fittedKey[i])) % 26)
    return vigenereDecrypted.lower()

def autoKeyVigenereEncrypt(plainText, key):
    plainText = stripNonLetterChars(plainText)
    fittedKey = key + plainText[:len(plainText) - len(key)]
    vigenereEncrypted = ''
    for i in range(len(plainText)):
        vigenereEncrypted += rankToLetter((letterToRank(plainText[i])  + letterToRank(fittedKey[i])) % 26)
    return vigenereEncrypted.upper()

def autoKeyVigenereDecrypt(cipherText, key):
    cipherText.lower()
    key = stripNonLetterChars(key)
    vigenereDecrypted = ''
    keyQueue = deque()
    for letter in key:
        keyQueue.append(letter)
    for i in range(len(cipherText)):
        currentLetterKey = keyQueue.popleft()
        currentPlainText = rankToLetter((letterToRank(cipherText[i])  - letterToRank(currentLetterKey)) % 26)
        keyQueue.append(currentPlainText)
        vigenereDecrypted += currentPlainText
    return vigenereDecrypted.lower()


def extendedVigenereEncrypt(plainText, key):
    fittedKey = fitKey(key, len(plainText))
    vigenereEncrypted = ''
    for i in range(len(plainText)):
        vigenereEncrypted += chr((ord(plainText[i])  + ord(fittedKey[i])) % 255)
    return vigenereEncrypted

def extendedVigenereDecrypt(cipherText, key):
    fittedKey = fitKey(key, len(cipherText))
    vigenereDecrypted = ''
    for i in range(len(cipherText)):
        vigenereDecrypted += chr((ord(cipherText[i])  - ord(fittedKey[i])) % 255)
    return vigenereDecrypted

def playfairEncrypt(plainText, key):
    playfairMatrix = constructPlayfairMatrix(key)
    playfairDict = makePlayfairDict(playfairMatrix)
    cipher = []
    for pairs in makePlayfairPlaintext(plainText):
        cipher += encodeLettersPlayfair(pairs, playfairDict, playfairMatrix)
    return ''.join(cipher)

def playfairDecrypt(cipherText, key):
    playfairMatrix = constructPlayfairMatrix(key)
    playfairDict = makePlayfairDict(playfairMatrix)
    decipher = []
    for pairs in makePlayfairCiphertext(cipherText):
        decipher += decodeLettersPlayfair(pairs, playfairDict, playfairMatrix)
    return ''.join(decipher)

def affineEncrypt(plainText, mKey, bKey):
    cipherText = ''
    plainText = stripNonLetterChars(plainText).lower()
    for letter in plainText:
        cipherText += rankToLetter((mKey*letterToRank(letter) + bKey) % 26)
    return cipherText.upper()

def affineDecrypt(cipherText, mKey, bKey):
    decipherText = ''
    mKeyInverse = inverseModulo(mKey, 26)
    for letter in cipherText:
        decipherText += rankToLetter((mKeyInverse*(letterToRank(letter)-bKey)) % 26)
    return decipherText.lower()