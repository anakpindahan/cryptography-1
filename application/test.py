from tkinter import *
from tkinter import filedialog as fd

import cryptoCommands

root = Tk()

root.title("Encrypt It")
root.geometry('480x400')

frame = Frame(root)
frame.grid()

def cipher():
    plainText = plainTextVar.get()
    key = keyVar.get()
    mKey = mKeyVar.get()
    bKey = bKeyVar.get()
    value = cipherVar.get()
    ciphered = ''
    if(value == 1):
        ciphered = cryptoCommands.vigenereEncrypt(plainText, key)
    elif(value == 2):
        ciphered = cryptoCommands.autoKeyVigenereEncrypt(plainText, key)
    elif(value == 3):
        ciphered = cryptoCommands.extendedVigenereEncrypt(plainText, key)
    elif(value == 4):
        ciphered = cryptoCommands.playfairEncrypt(plainText, key)
    elif(value == 5):
        ciphered = cryptoCommands.affineEncrypt(plainText, mKey, bKey)
    showTextVar.set(ciphered)
    showText.delete('1.0', END)
    showText.insert(END, showTextVar.get())

def decipher():
    cipherText = cipherTextVar.get()
    key = keyVar.get()
    mKey = mKeyVar.get()
    bKey = bKeyVar.get()
    value = cipherVar.get()
    deciphered = ''
    if(value == 1):
        deciphered = cryptoCommands.vigenereDecrypt(cipherText, key)
    elif(value == 2):
        deciphered = cryptoCommands.autoKeyVigenereDecrypt(cipherText, key)
    elif(value == 3):
        deciphered = cryptoCommands.extendedVigenereDecrypt(cipherText, key)
    elif(value == 4):
        deciphered = cryptoCommands.playfairDecrypt(cipherText, key)
    elif(value == 5):
        deciphered = cryptoCommands.affineDecrypt(cipherText, mKey, bKey)
    showTextVar.set(deciphered)
    showText.delete('1.0', END)
    showText.delete('1.0', END)
    showText.insert(END, showTextVar.get())

def buildKeyInput():
    cipherType = cipherVar.get()
    if(cipherType == 5):
        keyLabel.grid_remove()
        keyEntry.grid_remove()        
        mKeyLabel.grid()
        mKeyEntry.grid()
        bKeyLabel.grid()
        bKeyEntry.grid()
    else:
        mKeyLabel.grid_remove()
        mKeyEntry.grid_remove()
        bKeyLabel.grid_remove()
        bKeyEntry.grid_remove()        
        keyLabel.grid()
        keyEntry.grid()

def open_file_en():
    file = fd.askopenfile(mode = "r")
    if file is not None:
        plainTextVar.set(file.read())
    file.close()
    cipher()

def open_file_de():
    file = fd.askopenfile(mode = "r")
    if file is not None:
        cipherTextVar.set(file.read())
    file.close()
    decipher()

def open_file_en_by():
    file = fd.askopenfile(mode = "rb")
    if file is not None:
        plainTextVar.set(file.read())
    file.close()
    cipher()

def open_file_de_by():
    file = fd.askopenfile(mode = "rb")
    if file is not None:
        cipherTextVar.set(file.read())
    file.close()
    decipher()

cipherVar = IntVar()
plainTextVar = StringVar()
keyVar = StringVar()
cipherTextVar = StringVar()
mKeyVar = IntVar()
bKeyVar = IntVar()
showTextVar = StringVar()

normalVigenereButton = Radiobutton(root, text = 'Normal Vigenere', variable = cipherVar, value = 1, command = buildKeyInput)
normalVigenereButton.grid(row = 0, column = 0)

autoKeyVigenereButton = Radiobutton(root, text = 'Autokey Vigenere', variable = cipherVar, value = 2, command = buildKeyInput)
autoKeyVigenereButton.grid(row = 0, column = 1)

extendedVigenereButton = Radiobutton(root, text = 'Extended Vigenere', variable = cipherVar, value = 3, command = buildKeyInput)
extendedVigenereButton.grid(row = 0, column = 2)

playfairButton = Radiobutton(root, text = 'Playfair', variable = cipherVar, value = 4, command = buildKeyInput)
playfairButton.grid(row = 1, column = 0)

affineCipher = Radiobutton(root, text = 'Affine', variable = cipherVar, value = 5, command = buildKeyInput)
affineCipher.grid(row = 1, column = 2)

plainTextLabel = Label(root, text = 'Plain Text')
plainTextEntry = Entry(root, textvariable = plainTextVar)
plainTextLabel.grid(row = 2, column = 0)
plainTextEntry.grid(row = 3, column = 0)

encipherButton = Button(root, text = 'Encipher', command = cipher)
encipherButton.grid(row = 4, column = 0)

cipherTextLabel = Label(root, text = 'Cipher Text')
cipherTextEntry = Entry(root, textvariable = cipherTextVar)
cipherTextLabel.grid(row = 2, column = 2)
cipherTextEntry.grid(row = 3, column = 2)

decipherButton = Button(root, text = 'Decipher', command = decipher)
decipherButton.grid(row = 4, column = 2)

mKeyLabel = Label(root, text = "Key m")
mKeyEntry = Entry(root, textvariable = mKeyVar)
mKeyLabel.grid(row = 6, column = 0)
mKeyEntry.grid(row = 7, column = 0)

bKeyLabel = Label(root, text = "Key b")
bKeyEntry = Entry(root, textvariable = bKeyVar)
bKeyLabel.grid(row = 7, column = 2)
bKeyEntry.grid(row = 8, column = 2)

uploadEncipherButton = Button(root, text = 'Upload file', command = open_file_en)
uploadEncipherButton.grid(row = 5, column = 0)

uploadDecipherButton = Button(root, text = 'Upload file', command = open_file_de)
uploadDecipherButton.grid(row = 5, column = 2)

uploadEncipherByteButton = Button(root, text = 'Upload file as byte', command = open_file_en_by)
uploadEncipherByteButton.grid(row = 6, column = 0)

uploadDecipherByteButton = Button(root, text = 'Upload file as byte', command = open_file_de_by)
uploadDecipherByteButton.grid(row = 6, column = 2)

keyLabel = Label(root, text = "Key")
keyEntry = Entry(root, textvariable = keyVar)
keyLabel.grid(row = 7, column = 1)
keyEntry.grid(row = 8, column = 1)

keyLabel.grid_remove()
keyEntry.grid_remove()        
mKeyLabel.grid_remove()
mKeyEntry.grid_remove()
bKeyLabel.grid_remove()
bKeyEntry.grid_remove()

showText = Text(root, height = 20, width = 20)
showText.grid(row = 9, column = 1)

root.mainloop()

