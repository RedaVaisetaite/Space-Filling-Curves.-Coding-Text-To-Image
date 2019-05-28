__author__ = "Reda Vaisetaite"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2019/05/30 $"

import imageDecoding
import colorsys
from PIL import Image
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import imageEncoding
import os
from pathlib import Path
import EncodingFile
import DecodingFile

#stylesheets
StyleSheet = '''
QPushButton {
    background-color: #225891;
}

QPushButton:hover {
    background-color: #3781d1;
    color: #fff;
}
QPushButton:focus {
    background-color: #3781d1;
    color: #fff;
}
'''

StyleSheet1 = '''
QPushButton {
    background-color: #225891;
}

QPushButton:hover {
    background-color: #3781d1;
    color: #fff;
}
'''

# ----------------------------FUNCTIONS--------------------------------------

# get the biggest N, that is the number powered of 2 from image coordinates
def highestPowerof2(n):   
    res = 0 
    for i in range(n, 0, -1):           
        if ((i & (i - 1)) == 0):          
            res = i 
            break           
    return res 

# decoding algorithm for inputed text
def decodedCycle(N, textLength, bits, it, img_resized, rgbValue):
    decodedText = []
    if (bits == 2):
        nBits = 4
    elif (bits == 4 or bits == 6):
        nBits = 2
    elif (bits == 8):
        nBits = 1
    for i in range(0,N*N):
        if (it < textLength * nBits):
            letter = imageDecoding.hilbert2xy(i, N, textLength, bits, it, img_resized, rgbValue)
            m = it
            if (it >= textLength):
                m = it%textLength
                decodedText[m] = decodedText[m] + letter
            else:
                decodedText.append(letter)        
        it = it + 1
    return decodedText, it

# decoding for file
def decodeFile(N, bits, img_resized, rgbValue, newFile, filesize, nBits):
    for i in range(0,int(filesize*nBits),nBits):
        if bits == 2:
            first2bits = DecodingFile.hilbert2xy(i,N, 6, bits, img_resized, rgbValue)
            next2bits = DecodingFile.hilbert2xy(i+1,N, 4, bits, img_resized, rgbValue)
            next2bits1 = DecodingFile.hilbert2xy(i+2,N, 2, bits, img_resized, rgbValue)
            last2bits = DecodingFile.hilbert2xy(i+3,N, 0, bits, img_resized, rgbValue)  
            byte = first2bits + next2bits +  next2bits1 + last2bits
        elif (bits == 4):
            first2bits = DecodingFile.hilbert2xy(i,N, 4, bits, img_resized, rgbValue)
            next2bits = DecodingFile.hilbert2xy(i+1,N, 0, bits, img_resized, rgbValue)
            byte = first2bits + next2bits
        elif bits == 8:
            first2bits = DecodingFile.hilbert2xy(i,N, 0, bits, img_resized, rgbValue)
            byte = first2bits
        byte = bytes([byte])
        newFile.write(byte)

# encoding for file
def encodeFile(N, bits, img_resized, rgbValue, bytes_read):
    i = 0
    for byte in bytes_read:
        if bits == 2:
            EncodingFile.hilbert2xy(i,N, (byte&192), bits, 6, img_resized, rgbValue)
            EncodingFile.hilbert2xy(i+1,N, (byte&48), bits, 4, img_resized, rgbValue)
            EncodingFile.hilbert2xy(i+2,N, (byte&12), bits, 2, img_resized, rgbValue)
            EncodingFile.hilbert2xy(i+3,N, (byte&3), bits, 0, img_resized, rgbValue)
            i = i+4
        elif bits == 4:
            EncodingFile.hilbert2xy(i,N, (byte&240), bits, 4, img_resized, rgbValue)
            EncodingFile.hilbert2xy(i+1,N, (byte&15), bits, 0, img_resized, rgbValue)
            i = i + 2 
        elif bits == 8:
            EncodingFile.hilbert2xy(i,N, (byte&255), bits, 0, img_resized, rgbValue)
            i = i + 1
    

# -------------------------------GUI FUNCTIONS---------------------------------------
# main class for Window and all widgets functions
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi('gui.ui',self)
        self.setWindowTitle('Erdvę užpildančios kreivės')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.about.clicked.connect(self.about_clicked)
        self.about.setStyleSheet(StyleSheet)
        self.compareImage.setStyleSheet(StyleSheet1)
        self.decodedMenu.setStyleSheet(StyleSheet)
        self.encodedMenu.setStyleSheet(StyleSheet)
        self.browse.setStyleSheet(StyleSheet1)
        self.browse.setStyleSheet(StyleSheet1)
        self.encode.setStyleSheet(StyleSheet1)
        self.decode.setStyleSheet(StyleSheet1)
        self.compare.setStyleSheet(StyleSheet1)
        self.decodedMenu.clicked.connect(self.decodedMenu_clicked)
        self.encodedMenu.clicked.connect(self.encodedMenu_clicked)
        self.decode.clicked.connect(self.decodeButton_clicked)
        self.compareImage.clicked.connect(self.compareImage_clicked)
        self.encode.clicked.connect(self.encodeButton_clicked)
        self.browse.clicked.connect(self.getImage)
        self.browse2.clicked.connect(self.getImage2)
        self.browseFile.clicked.connect(self.getFile)
        self.chooseResultFile.clicked.connect(self.saveFile)
        self.compare.clicked.connect(self.compareMenu_clicked)
        self.textEdit.textChanged.connect(self.textChangedCount)
        self.progressBar.setVisible(False)
        self.RGBcomboBox.setStyleSheet('color: white; font: 10pt "Microsoft YaHei"')
        self.radioButtonText.toggled.connect(self.radioButtonTextPressed)
        self.radioButtonFile.toggled.connect(self.radioButtonFilePressed)
        self.dradioButtonText.toggled.connect(self.dradioButtonTextPressed)
        self.dradioButtonFile.toggled.connect(self.dradioButtonFilePressed)
        self.chooseDecode.clicked.connect(self.getDecodeName)
        self.RGBcomboBox.currentTextChanged.connect(self.symbolsCounting)
        self.bitsComboBox.currentTextChanged.connect(self.symbolsCounting)
        self.imagename.textChanged.connect(self.symbolsCounting)
        self.resultFileName.setDisabled(True)
        self.decodedname.setDisabled(True)
        self.imagename.setDisabled(True)
        self.imagename.setDisabled(True)
        self.encodeFileName.setDisabled(True)
    @pyqtSlot()

    # decode button function
    def decodeButton_clicked(self):  
        self.resultFileName.setDisabled(True)
        textLength = self.textLength.value()
        imagePath = self.imagepath.text()       

        if Path(imagePath).is_file():
            img = Image.open(imagePath)

            #load pixels
            img_resized = img.load()
            [xs, ys] = img.size

            rgbValue = str(self.RGBcomboBox.currentText())
            N = highestPowerof2(min(xs,ys))

            # get bits from user 
            bits = int(self.bitsComboBox.currentText())

            # counting how many symbols can to encode by bits
            if (bits == 2):
                symbolsCount = int(N*N/4)
                nBits = 4
            elif (bits == 4 or bits == 6):
                symbolsCount = int(N*N/2)
                nBits = 2
            elif (bits == 8):
                symbolsCount = int(N*N)
                nBits = 1

            # check file or text need to encode
            if self.dradioButtonFile.isChecked() == True:
                file = 1
            else:
                file = 0

            if file == 1:

                # for file coding
                resultFile = str(self.resultFileName.text())
                outputfile = resultFile
                if not outputfile:
                    outputfile = os.path.expanduser("~/Desktop/result.txt")
                newFile = open(outputfile, "wb")
                filesize=int(self.textLength.value())
                if (rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b'):
                    decodeFile(N, bits, img_resized, rgbValue, newFile, filesize, nBits)

                elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'g b':
                    rgbValue = rgbValue.split(' ')
                    if (filesize>symbolsCount):
                        filesize1 = symbolsCount
                        decodeFile(N, bits, img_resized, rgbValue[0], newFile, filesize1, nBits)
                        filesize2 = int(filesize - filesize1)
                        decodeFile(N, bits, img_resized, rgbValue[1], newFile, filesize2, nBits)
                    else:
                        filesize1 = filesize
                        decodeFile(N, bits, img_resized, rgbValue[0], newFile, filesize1, nBits)                            
                        
                elif (rgbValue == 'r g b'):
                    rgbValue = rgbValue.split(' ')
                    if (filesize>symbolsCount):
                        filesize1 = symbolsCount
                    else:
                        filesize1 = filesize
                    decodeFile(N, bits, img_resized, rgbValue[0], newFile, filesize1, nBits)
                    if (filesize>symbolsCount):
                        if (filesize>(symbolsCount*2)):
                            decodeFile(N, bits, img_resized, rgbValue[1], newFile, filesize1, nBits)
                        else:
                            filesize1 = int(symbolsCount*2 - filesize)
                            decodeFile(N, bits, img_resized, rgbValue[1], newFile, filesize1, nBits)
                    if (filesize>(symbolsCount*2)):
                        filesize2 = int(filesize - (filesize1*2))
                        decodeFile(N, bits, img_resized, rgbValue[2], newFile, filesize2, nBits) 

                # print result to the screen for user
                self.result.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                    font: 10pt "Microsoft YaHei"')
                self.result.setText("Failas dekoduotas. Jis yra išsaugotas \n" + outputfile)
            #self.textEdit.setDisabled(True)
                self.result.setVisible(True)      

            # decoding text from input
            else:
                decodedText = []
                it = 0        
                if rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b':
                    if (textLength > symbolsCount):
                        textLength = symbolsCount
                    decodedText, it = decodedCycle(N, textLength, bits, it, img_resized, rgbValue)

                elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'g b':
                    rgbValue = rgbValue.split(' ')
                    # decoding just in first color, if text length is less than symbolsCount
                    if (textLength <= symbolsCount):
                        decodedText, it = decodedCycle(N, textLength, bits, it, img_resized, rgbValue[0])

                    else:     
                        lastText = textLength - symbolsCount
                        lastText = int(lastText)
                        if (textLength > int(symbolsCount*2)):
                            lastText = int(symbolsCount)
                        nextletter = symbolsCount
                        it1 = 0
                        it2 = lastText  

                        # encode symbolsCount text length in first color
                        decodedText, it = decodedCycle(N, int(symbolsCount), bits, it, img_resized, rgbValue[0]) 
                    
                        for i in range(0,N*N):
                            if (it1 < lastText * nBits):
                                # encode last text in second color
                                letter = imageDecoding.hilbert2xy(i, N, lastText, bits, it1, img_resized, rgbValue[1])                         
                                m = it1
                                if (nextletter >= textLength):                                
                                    if (it1==lastText*2):
                                        it2 = it2 + lastText
                                    elif (it1==lastText*3):
                                        it2 = it2 + lastText
                                    m = int(nextletter - it2)
                                    decodedText[m] = decodedText[m] + letter
                                else:
                                    decodedText.append(letter)      
                            it1 = it1 + 1
                            it = it + 1
                            nextletter = nextletter + 1 

                elif (rgbValue == 'r g b'):
                    rgbValue = rgbValue.split(' ') 

                    lastText = 0
                    lastText2 = 0

                    # count text for each color
                    if (textLength > symbolsCount and textLength <= (symbolsCount*2)):
                        lastText = textLength - symbolsCount
                    elif (textLength > symbolsCount and textLength > (symbolsCount*2)):
                        lastText = symbolsCount
                        lastText2 = textLength - symbolsCount*2
                    elif (textLength>int(symbolsCount*3)):
                        lastText = symbolsCount
                        lastText2 = symbolsCount

                    if (textLength < symbolsCount): 
                        decodedText, it = decodedCycle(N, textLength, bits, it, img_resized, rgbValue[0])

                    lastText = int(lastText)
                    nextletter = symbolsCount
                    nextletter2 = symbolsCount*2
                    it1 = 0
                    it2 = lastText
                    it3 = lastText2
                    it4 = 0 

                    if (textLength >= symbolsCount):
                        decodedText, it = decodedCycle(N, int(symbolsCount), bits, it, img_resized, rgbValue[0])   

                        for i in range(0,N*N):
                            if (it1 < lastText * nBits):
                                letter = imageDecoding.hilbert2xy(i, N, lastText, bits, it1, img_resized, rgbValue[1])                           
                                m = it1
                                gg = 0
                                if (textLength>=int(symbolsCount*2)):
                                    gg = int(symbolsCount*2)
                                else:
                                    gg = textLength
                                if (nextletter >= gg):                                
                                    if (it1==lastText*2):
                                        it2 = it2 + lastText
                                    elif (it1==lastText*3):
                                        it2 = it2 + lastText
                                    m = int(nextletter - it2)
                                    decodedText[m] = decodedText[m] + letter
                                else:
                                    decodedText.append(letter)     
                            it1 = it1 + 1
                            it = it + 1
                            nextletter = nextletter + 1

                    if (textLength >= symbolsCount*2): 
                        for i in range(0,N*N):
                            if (it4 < lastText2 * nBits):
                                letter = imageDecoding.hilbert2xy(i, N, lastText2, bits, it4, img_resized, rgbValue[2])                        
                                m = it4
                                if (textLength>=int(symbolsCount*3)):
                                    textLength = int(symbolsCount*3)
                                if (nextletter2 >= textLength):                                
                                    if (it4==lastText2*2):
                                        it3 = it3 + lastText2
                                    elif (it4==lastText2*3):
                                        it3 = it3 + lastText2
                                    m = int(nextletter2 - it3)
                                    decodedText[m] = decodedText[m] + letter
                                else:
                                    decodedText.append(letter)       
                            it4 = it4 + 1
                            it = it + 1
                            nextletter2 = nextletter2 + 1


                text = ''
                if (decodedText != []):
                    for letter in decodedText:
                        text = text + chr(letter)
                # print decoded text to user
                self.result.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                    font: 10pt "Microsoft YaHei"')
                self.result.setText("Dekoduotas tekstas: \n"+text)
                self.result.setVisible(True)
        else:
            self.symbols.setText("Paveikslėlis, kurį pasirinkote nerastas.\
 Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)")
            self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)

    def compareImage_clicked(self):
        imageencoded = self.imagepath.text()
        imagedecoded = self.decodedname.text()
        Dialog = QtWidgets.QDialog()
        loadUi('ImageShow.ui', Dialog)
        pixmapEncoded = QPixmap(imageencoded)
        pixmapDecoded = QPixmap(imagedecoded)
        Dialog.image1.setPixmap(QPixmap(pixmapEncoded))
        Dialog.image1.resize(pixmapEncoded.width(), pixmapEncoded.height())
        Dialog.image2.setPixmap(QPixmap(pixmapDecoded))
        Dialog.image2.resize(pixmapDecoded.width(), pixmapDecoded.height())    
        Dialog.show()
        Dialog.exec_()

    def encodeButton_clicked(self):
        self.symbols.setText("")
        self.textCoded.setVisible(False)
        imagePath = self.imagename.text()

        # for symbols counting
        rgbMatrix = {
            'r': 1,
            'g': 1,
            'b': 1,
            'r g': 2,
            'r b': 2,
            'g b': 2,
            'r g b': 3
        } 

        if Path(imagePath).is_file():
            img = Image.open(imagePath)
            img_resized = img.load() #load pixels
            [xs,ys] = img.size

            N = highestPowerof2(min(xs,ys))

            #get information from user
            bits = int(self.bitsComboBox.currentText()) 
            rgbValue = str(self.RGBcomboBox.currentText())
            text = self.textEdit.toPlainText()
            textLength = len(text)

            if (bits == 2):
                symbolsCount = int(N*N/4)
                nBits = 4
            elif (bits == 4 or bits == 6):
                symbolsCount = int(N*N/2)
                nBits = 2
            elif (bits == 8):
                symbolsCount = int(N*N)
                nBits = 1  

            fileCount = int(symbolsCount*rgbMatrix[rgbValue])          

            it = 0
            it1 = 0
            it2 = 0
            
            if self.radioButtonFile.isChecked() == True :
                isFile = 1
            else:
                isFile = 0

            # encoding file
            if isFile == 1:
                if not self.encodeFileName.text():
                    self.symbols.setText("Paveisklėlis, kurį pasirinkote nerastas.\
                    Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)")
                    self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
                    self.symbols.setVisible(True)
                else: 
                    file = self.filePath.text()
                    filesize = os.path.getsize(file)
                    bytes_read = open(file, "rb")
                    if (filesize>fileCount):
                        self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
                        self.symbols.setText("Failas yra per didelis. Pasirinkite mažesnį failą arba didesnę nuotrauką kodavimui. \n"+\
                            "Taip pat galite nustatyti kitus parametrus.")
                    else:
                        if rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b':
                            bytes_read = bytes_read.read()
                            encodeFile(N, bits, img_resized, rgbValue, bytes_read)                            
                        elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'g b':
                            rgbValue = rgbValue.split(' ')
                            if (filesize>symbolsCount):
                                bytes_read1 = bytes_read.read(symbolsCount)
                                encodeFile(N, bits, img_resized, rgbValue[0], bytes_read1)
                                bytes_read.seek(symbolsCount,0)
                                bytes_read2 = bytes_read.read()
                                encodeFile(N, bits, img_resized, rgbValue[1], bytes_read2)
                            else:
                                bytes_read1 = bytes_read.read()
                                encodeFile(N, bits, img_resized, rgbValue[0], bytes_read1)
                        
                        elif rgbValue == 'r g b':
                            rgbValue = rgbValue.split(' ')
                            bytes_read1 = bytes_read.read(symbolsCount)
                            encodeFile(N, bits, img_resized, rgbValue[0], bytes_read1)
                            bytes_read.seek(symbolsCount,0)
                            bytes_read2 = bytes_read.read()
                            encodeFile(N, bits, img_resized, rgbValue[1], bytes_read2)
                            bytes_read.seek(int(symbolsCount*2),0)
                            bytes_read3 = bytes_read.read()
                            encodeFile(N, bits, img_resized, rgbValue[2], bytes_read3)
                        # get the feedback to user
                        if not self.decodedname.text() or not self.decodedname.text().lower().endswith('.png'):
                            decodedname = os.path.expanduser("~/Desktop/test.png")
                        else:
                            decodedname = self.decodedname.text()
                        img.save(decodedname)
                        self.textEdit.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                            font: 10pt "Microsoft YaHei"')
                        self.textEdit.setText("Failas užkoduotas.\nUžkoduoto failo dydis baitais: "+str(filesize)+
                            "\nUžkoduotas paveikslėlis išsaugotas "+decodedname)
                        self.textEdit.setVisible(True)
                self.compareImage.setVisible(True)

            # encoding text from input
            else:
                if rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b':
                    if (len(text) > symbolsCount):
                        text = text[:int(symbolsCount)]
                        textLength = symbolsCount
                    for i in range(0,N*N):  
                        if (it < len(text) * nBits):
                            imageEncoding.hilbert2xy(i,N, text, bits, it, img_resized, rgbValue)
                            it = it + 1

                elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'g b':
                    rgbValue = rgbValue.split(' ') 

                    if (it < len(text) * nBits):
                        if (len(text) <= symbolsCount):
                            for i in range(0,N*N):
                                if (it < len(text) * nBits):
                                    imageEncoding.hilbert2xy(i,N, text, bits, it, img_resized, rgbValue[0])
                                    it = it + 1
                        else:
                            text1 = text[:int(symbolsCount)]
                            textLast = text[int(symbolsCount):]
                            if (len(text) > (symbolsCount*2)):
                                textLast = text[int(symbolsCount):int(symbolsCount*2)]
                                textLength = int(symbolsCount*2)

                            for i in range(0,N*N):
                                if (it < len(text1) * nBits):
                                    imageEncoding.hilbert2xy(i,N, text1, bits, it, img_resized, rgbValue[0])
                                    it = it + 1

                            for i in range(0,N*N):
                                if (it < len(textLast) * nBits):
                                    imageEncoding.hilbert2xy(i,N, textLast, bits, it1, img_resized, rgbValue[1])
                                    it = it + 1 
                                    it1 = it1 + 1

                elif rgbValue == 'r g b':
                    rgbValue = rgbValue.split(' ')

                    if (it < len(text) * nBits):
                        text1 = ''
                        text2 = ''
                        textLast = ''
                        if (len(text) > symbolsCount and len(text) <= (symbolsCount*2)):
                            text1 = text[:int(symbolsCount)]
                            text2 = text[int(symbolsCount):]
                        elif (len(text) > symbolsCount and len(text) > (symbolsCount*2)):
                            text1 = text[:int(symbolsCount)]
                            text2 = text[int(symbolsCount):int(symbolsCount*2)]
                            textLast = text[int(symbolsCount*2):]
                            if (len(text) > (symbolsCount*3)): 
                                textLast = text[int(symbolsCount*2):int(symbolsCount*3)]
                                textLength = int(symbolsCount*3)

                        if (len(text) > symbolsCount):                       
                            for i in range(0,N*N):
                                if (it < len(text1) * nBits):
                                    imageEncoding.hilbert2xy(i,N, text1, bits, it, img_resized, rgbValue[0])
                                    it = it + 1

                            for i in range(0,N*N):
                                if (it < len(text2) * nBits):
                                    imageEncoding.hilbert2xy(i,N, text2, bits, it1, img_resized, rgbValue[1])
                                    it = it + 1 
                                    it1 = it1 + 1

                        if (len(text) > symbolsCount*2):
                            for i in range(0,N*N):
                                if (it < len(textLast) * nBits):
                                    imageEncoding.hilbert2xy(i,N, textLast, bits, it2, img_resized, rgbValue[2])
                                    it = it + 1 
                                    it2 = it2 + 1

                        if (len(text) < symbolsCount):
                            for i in range(0,N*N):
                                if (it < len(text) * nBits):
                                    imageEncoding.hilbert2xy(i,N, text, bits, it, img_resized, rgbValue[0])
                                    it = it + 1

                # get the feedback to user
                if not self.decodedname.text() or not self.decodedname.text().lower().endswith('.png'):
                    decodedname = os.path.expanduser("~/Desktop/test.png")
                else:
                    decodedname = self.decodedname.text()
                img.save(decodedname)
                self.textEdit.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                font: 10pt "Microsoft YaHei"')
                self.textEdit.setText("Užkoduoto teksto ilgis: "+str(textLength)+
"\nUžkoduotas paveikslėlis išsaugotas "+decodedname+
"\nUžkoduotas tekstas: "+text[:textLength])
                self.textEdit.setVisible(True)
                self.compareImage.setVisible(True)
        else:
            self.symbols.setText("Paveikslėlis, kurį pasirinkote nerastas.\
 Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)")
            self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)

    # main button function
    def about_clicked(self):
        self.labelImage.setVisible(False)
        self.symbols.setVisible(False)
        self.labelName.setVisible(False)
        self.decodedname.setVisible(False)
        self.compareImage.setVisible(False)
        self.label1.setVisible(False)
        self.encode.setVisible(False)
        self.textEdit.setVisible(False)
        self.textLength.setVisible(False)
        self.decode.setVisible(False)
        self.browse.setVisible(False)
        self.imagename.setVisible(False)
        self.label.setVisible(False)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(True)
        self.RGBcomboBox.setVisible(False)
        self.rgbLabel.setVisible(False)
        self.textCoded.setVisible(False)
        self.bitsLabel.setVisible(False)
        self.bitsComboBox.setVisible(False)
        self.browse2.setVisible(False)
        self.imageName2.setVisible(False)
        self.radioButtonText.setVisible(False)
        self.radioButtonFile.setVisible(False)
        self.radioButtonLabel.setVisible(False)
        self.dradioButtonText.setVisible(False)
        self.dradioButtonFile.setVisible(False)
        self.dradioButtonLabel.setVisible(False)
        self.resultFileName.setVisible(False)
        self.resultFileLabel.setVisible(False)
        self.browseFile.setVisible(False)
        self.fileBrowserLabel.setVisible(False)
        self.encodeFileName.setVisible(False)
        self.chooseResultFile.setVisible(False)
        self.chooseDecode.setVisible(False)

    def decodedMenu_clicked(self):
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setText("Pasirinkite norimą dekoduoti paveikslėlį")  
        self.labelImage.setVisible(True)
        self.symbols.setVisible(False)
        self.labelName.setVisible(False)
        self.decodedname.setVisible(False)
        self.compareImage.setVisible(False)
        self.encode.setVisible(False)
        self.label1.setVisible(False)
        self.textEdit.setVisible(False)
        self.textLength.setVisible(True)
        self.decode.setVisible(True)
        self.browse.setVisible(True)
        self.imagename.setVisible(True)
        self.label.setVisible(True)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        self.RGBcomboBox.setVisible(True)
        self.rgbLabel.setVisible(True)
        self.textCoded.setVisible(False)
        self.bitsLabel.setVisible(True)
        self.bitsComboBox.setVisible(True)
        self.browse2.setVisible(False)
        self.imageName2.setVisible(False)
        self.radioButtonText.setVisible(False)
        self.radioButtonFile.setVisible(False)
        self.radioButtonLabel.setVisible(False)
        self.browseFile.setVisible(False)
        self.fileBrowserLabel.setVisible(False)
        self.encodeFileName.setVisible(False)
        self.dradioButtonText.setVisible(True)
        self.dradioButtonFile.setVisible(True)
        self.dradioButtonLabel.setVisible(True)
        self.resultFileName.setVisible(True)
        self.resultFileLabel.setVisible(True)
        self.chooseDecode.setVisible(False)
        if self.dradioButtonText.isChecked() == True:
            self.resultFileName.setVisible(False)
            self.chooseResultFile.setVisible(False)
            self.resultFileLabel.setVisible(False)
        if self.dradioButtonFile.isChecked() == True:
            self.resultFileName.setDisabled(True)
            self.resultFileName.setVisible(True)
            self.resultFileLabel.setVisible(True)
            self.chooseResultFile.setVisible(True)


    def encodedMenu_clicked(self):
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setText("Pasirinkite paveikslėlį, kuris bus naudojamas kodavimui")        
        self.labelImage.setVisible(True)
        self.symbols.setVisible(False)
        self.labelName.setVisible(True)
        self.decodedname.setDisabled(True)
        self.decodedname.setVisible(True)
        self.compareImage.setVisible(False)
        self.textLength.setVisible(False)
        self.decode.setVisible(False)
        self.encode.setVisible(True)
        self.browse.setVisible(True)
        self.imagename.setVisible(True)
        self.label.setVisible(False)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        self.RGBcomboBox.setVisible(True)
        self.rgbLabel.setVisible(True)        
        self.bitsLabel.setVisible(True)
        self.bitsComboBox.setVisible(True)
        self.browse2.setVisible(False)
        self.imageName2.setVisible(False)
        self.radioButtonText.setVisible(True)
        self.radioButtonFile.setVisible(True)
        self.radioButtonLabel.setVisible(True)
        self.browseFile.setVisible(True)
        self.fileBrowserLabel.setVisible(True)
        self.encodeFileName.setVisible(True)
        self.browseFile.setVisible(False)
        self.fileBrowserLabel.setVisible(False)
        self.encodeFileName.setVisible(False)
        self.dradioButtonText.setVisible(False)
        self.dradioButtonFile.setVisible(False)
        self.dradioButtonLabel.setVisible(False)
        self.resultFileName.setVisible(False)
        self.chooseResultFile.setVisible(False)
        self.resultFileLabel.setVisible(False)
        self.chooseDecode.setVisible(True)
        self.textEdit.setText("")
        if self.radioButtonText.isChecked() == True:
            self.label1.setVisible(True)
            self.textEdit.setVisible(True)
            self.textCoded.setVisible(True)
        if self.radioButtonFile.isChecked() == True:
            self.browseFile.setVisible(True)
            self.fileBrowserLabel.setVisible(True)
            self.encodeFileName.setVisible(True)
            self.textCoded.setVisible(False)
        
        
    def getImage(self):

      cwd = os.getcwd()
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            cwd, "Image files (*.jpg *.jpeg, *.png)")
      if Path(fname[0]).is_file():
        imagePath = fname[0]
        imageName = imagePath.split("/")[-1]
        self.imagename.setText(imagePath)
        self.imagepath.setText(imagePath)

    def getImage2(self):
      cwd = os.getcwd()
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            cwd, "Image files (*.jpg *.jpeg, *.png)")
      if Path(fname[0]).is_file():
        imagePath = fname[0]
        imageName = imagePath.split("/")[-1]
        self.decodedname.setText(imagePath)
        self.imagePath2.setText(imagePath)


    def compareMenu_clicked(self):
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setText("Pasirinkite pirmąjį paveikslėlį")        
        self.labelImage.setVisible(True)
        self.labelName.setVisible(False)
        self.symbols.setVisible(False)
        self.imageName2.setVisible(True)
        self.decodedname.setVisible(True)
        self.compareImage.setVisible(True)
        self.textLength.setVisible(False)
        self.textEdit.setVisible(False)
        self.decode.setVisible(False)
        self.encode.setVisible(False)
        self.browse.setVisible(True)
        self.imagename.setVisible(True)
        self.label.setVisible(False)
        self.label1.setVisible(False)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        self.RGBcomboBox.setVisible(False)
        self.rgbLabel.setVisible(False)
        self.textCoded.setVisible(False)
        self.bitsLabel.setVisible(False)
        self.bitsComboBox.setVisible(False)
        self.browse2.setVisible(True)
        self.radioButtonText.setVisible(False)
        self.radioButtonFile.setVisible(False)
        self.radioButtonLabel.setVisible(False)
        self.browseFile.setVisible(False)
        self.fileBrowserLabel.setVisible(False)
        self.encodeFileName.setVisible(False)
        self.dradioButtonText.setVisible(False)
        self.dradioButtonFile.setVisible(False)
        self.dradioButtonLabel.setVisible(False)
        self.resultFileName.setVisible(False)
        self.resultFileLabel.setVisible(False)
        self.chooseResultFile.setVisible(False)
        self.chooseDecode.setVisible(False)

    def textChangedCount(self):
        self.textCoded.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                font: 10pt "Microsoft YaHei"')
        self.textCoded.setText("Jau įvedėte "+str(len(self.textEdit.toPlainText()))+" simbolį (-ius)")

    def symbolsCounting(self):
        rgbMatrix = {
            'r': 1,
            'g': 1,
            'b': 1,
            'r g': 2,
            'r b': 2,
            'g b': 2,
            'r g b': 3
        } 
        bits = int(self.bitsComboBox.currentText())
        if (bits == 2):
            nBits = 4
        elif (bits == 4 or bits == 6):
            nBits = 2
        elif (bits == 8):
            nBits = 1

        if self.imagename.text() and self.labelImage.text()=="Pasirinkite paveikslėlį, kuris bus naudojamas kodavimui":
            imagePath = self.imagename.text() 
            img = Image.open(imagePath)
            img_resized = img.load() #uzsikraunam pikselius
            [xs,ys] = img.size
            N = highestPowerof2(min(xs,ys))
            rgb = rgbMatrix[self.RGBcomboBox.currentText()]
            symbolsCount = int(N*N)*rgb/nBits
            self.symbols.setText('Maksimalus simbolių skaičius, kurį galite užkoduoti yra '+str(int(symbolsCount))+\
                ' baitas(-i)/simbolis(-ai)')
            self.symbols.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)

    def radioButtonFilePressed(self):
        self.label1.setVisible(False)
        self.textEdit.setVisible(False)
        self.browseFile.setVisible(True)
        self.fileBrowserLabel.setVisible(True)
        self.encodeFileName.setVisible(True)
        self.textCoded.setVisible(False)

    def radioButtonTextPressed(self):
        self.label1.setVisible(True)
        self.textEdit.setVisible(True)
        self.browseFile.setVisible(False)
        self.fileBrowserLabel.setVisible(False)
        self.encodeFileName.setVisible(False)
        self.textCoded.setVisible(True)

    def dradioButtonFilePressed(self):
        self.resultFileLabel.setVisible(True)
        self.resultFileName.setVisible(True)
        self.chooseResultFile.setVisible(True)

    def dradioButtonTextPressed(self):
        self.resultFileLabel.setVisible(False)
        self.resultFileName.setVisible(False)
        self.chooseResultFile.setVisible(False)

    def getFile(self):
      cwd = os.getcwd()
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            cwd, "All files (*.*)")
      if Path(fname[0]).is_file():
        filePath = fname[0]
        fileName = filePath.split("/")[-1]
        self.encodeFileName.setText(fileName)
        self.filePath.setText(filePath)

    def saveFile(self):
        cwd = os.getcwd()
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as... File', './')
        self.resultFileName.setText(str(fname[0]))

    def getDecodeName(self):
        cwd = os.getcwd()
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as... File', './', 'png(*.png)')
        self.decodedname.setText(str(fname[0]))
        self.imagepathDecoded.setText(str(fname[0]))      

app = QtWidgets.QApplication(sys.argv)
gui = Window()
gui.show()
sys.exit(app.exec_())
