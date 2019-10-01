from appJar import gui
import json
import binascii
import os

directory = ""
currentDir = ""
currentMax = 0
currentVal = 0


def updateProgress():
    global currentDir
    global currentMax
    global currentVal

    if currentMax != 0:
        app.setMeter("progressbar", currentVal/currentMax)
    app.setMessage("title", currentDir)

def xor(data, key):
    l = len(key)
    return bytearray(((data[i] ^ key[i % l]) for i in range(0,len(data))))

def getEncryptionKey(directory):
    path = directory + "/www/data/System.json"
    try:
        with open(path, "r") as json_file:
            data = json.load(json_file)
            return data["encryptionKey"]
    except:
        app.errorBox("Error", "Unable to find " + directory + "/www/data/System.json")
    return None

def decryptFile(filename, key):
    key = binascii.unhexlify(key)
    fileIn = open(filename, "rb")
    file = fileIn.read()
    file = file[16:]
    encData = bytearray(file[:16])
    decData = xor(encData, key)
    file = file[16:]
    
    if filename.endswith("o"):
        filename = filename[:-7] + ".ogg"
    elif filename.endswith("m"):
        filename = filename[:-7] + ".m4a"
    elif filename.endswith("p"):
        filename = filename[:-7] + ".png"
    
    outFile = open(filename, "wb")
    outFile.write(decData)
    outFile.write(file)

    outFile.close()
    fileIn.close()

    return

def decrypt():
    global directory
    global currentDir
    global currentMax
    global currentVal

    key = getEncryptionKey(directory)
    
    if key is not None:
        for path, dirs, files in os.walk(directory + "/www"):
            currentVal = 0
            currentMax = len(files)
            currentDir = path
            for f in files:
                if(f.endswith((".rpgmvo", ".rpgmvm", ".rpgmvp"))):
                    currentVal += 1
                    decryptFile(os.path.join(path, f), key)
    else:
        app.errorBox("Error", "Unable to find the encryption key.")

    return

def buttonPressed(button):
    global directory
    if button == "Browse":
        directory = app.directoryBox("Root directory of the game")
    else:
        decrypt()


app  = gui("RPGM Decode", "400x200")
app.addButtons(["Browse", "Decrypt"], buttonPressed)
app.addMessage("title", "")
app.addMeter("progressbar")
app.registerEvent(updateProgress)


app.go()
