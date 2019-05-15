import imagereadDecoding
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import colorsys
from PIL import Image
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import imagereadEncoding
import os
from pathlib import Path

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
def highestPowerof2(n): 
  
    res = 0; 
    for i in range(n, 0, -1): 
          
        # If i is a power of 2 
        if ((i & (i - 1)) == 0): 
          
            res = i; 
            break; 
          
    return res; 
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi('gui.ui',self)
        self.setWindowTitle('Erdvę užpildančios kreivės')
        self.about.clicked.connect(self.about_clicked)
        self.about.setStyleSheet(StyleSheet)
        self.compareImage.setStyleSheet(StyleSheet1)
        self.decodedMenu.setStyleSheet(StyleSheet)
        self.encodedMenu.setStyleSheet(StyleSheet)
        self.browse.setStyleSheet(StyleSheet1)
        self.encode.setStyleSheet(StyleSheet1)
        self.decode.setStyleSheet(StyleSheet1)
        self.compare.setStyleSheet(StyleSheet1)
        self.imagename.setText("Įveskite kelią")
        self.decodedMenu.clicked.connect(self.decodedMenu_clicked)
        self.encodedMenu.clicked.connect(self.encodedMenu_clicked)
        self.decode.clicked.connect(self.decodeButton_clicked)
        self.compareImage.clicked.connect(self.compareImage_clicked)
        self.encode.clicked.connect(self.encodeButton_clicked)
        self.browse.clicked.connect(self.getImage)
        self.RGBcomboBox.setStyleSheet('color: white; font: 10pt "Microsoft YaHei"')
    @pyqtSlot()
    
    def decodeButton_clicked(self):
        
        textLength = self.textLength.value()
        imagePath = self.imagepath.text()
        if Path(imagePath).is_file():
            img = Image.open(imagePath)
            #uzsikraunam pikselius
            img_resized = img.load()
            [xs, ys] = img.size
            # img = img_file.resize((256, 256), Image.ANTIALIAS)

         
            N = highestPowerof2(min(xs,ys))
            symbolsCount = N*N/4
            decodedText = []
            it = 0
            rgbValue = str(self.RGBcomboBox.currentText())
            # rgbValue = 'r g'
            if rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b':
                for i in range(0,N*N):
                    if (it < textLength * 4):
                        letter = imagereadDecoding.hilbert2xy(i, N, textLength, 2, it, img_resized, rgbValue)
                        m = it
                        if (it >= textLength):
                            m = it%textLength
                            decodedText[m] = decodedText[m] + letter
                        else:
                            decodedText.append(letter)        
                    it = it + 1
            elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'b g':
                rgbValue = rgbValue.split(' ')
                if (textLength <= symbolsCount):
                    for i in range(0,N*N):
                        if (it < textLength * 4):
                            letter = imagereadDecoding.hilbert2xy(i, N, textLength, 2, it, img_resized, rgbValue[0])
                            m = it
                            if (it >= textLength):
                                m = it%textLength
                                decodedText[m] = decodedText[m] + letter
                            else:
                                decodedText.append(letter)        
                        it = it + 1
                else:     
                    lastText = textLength - symbolsCount
                    lastText = int(lastText)
                    nextletter = symbolsCount
                    it1 = 0
                    it2 = lastText 
                    for i in range(0,N*N):
                        if (it < (textLength-lastText) * 4):
                            letter = imagereadDecoding.hilbert2xy(i, N, int(textLength-lastText), 2, it, img_resized, rgbValue[0])
                            m = it
                            # print(m)
                            if (it >= symbolsCount):
                                m = int(it%symbolsCount)
                                # print(m)
                                decodedText[m] = decodedText[m] + letter
                            else:
                                decodedText.append(letter)        
                        it = it + 1   
                    
                    for i in range(0,N*N):
                        #print('nextvisad ', nextletter)
                        if (it1 < lastText * 4):
                            #print(it1)
                            letter = imagereadDecoding.hilbert2xy(i, N, lastText, 2, it1, img_resized, rgbValue[1])
                                #m = it1                            
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
                                #print('pirma',m)       
                        it1 = it1 + 1
                        it = it + 1
                        nextletter = nextletter + 1 
            elif (rgbValue == 'r g b'):
                rgbValue = rgbValue.split(' ')
                
                lastText = 0
                lastText2 = 0
                if (textLength > symbolsCount and textLength <= (symbolsCount*2)):
                    lastText = textLength - symbolsCount
                elif (textLength > symbolsCount and textLength > (symbolsCount*2)):
                    lastText = symbolsCount
                    lastText2 = textLength - symbolsCount*2
                if (textLength < symbolsCount): 
                    print('textLength ', textLength)
                    for i in range(0,N*N):
                    # print('pirmas for veikia')
                        if (it < textLength * 4):
                            letter = imagereadDecoding.hilbert2xy(i, N, textLength, 2, it, img_resized, rgbValue[0])
                            m = it
                        # print(m)
                            if (it >= textLength):
                                m = int(it%textLength)
                            # print(m)
                                decodedText[m] = decodedText[m] + letter
                            else:
                                decodedText.append(letter)        
                        it = it + 1

                lastText = int(lastText)
                nextletter = symbolsCount
                nextletter2 = symbolsCount*2
                it1 = 0
                it2 = lastText
                it3 = lastText2
                it4 = 0 
                if (textLength >= symbolsCount):
                    for i in range(0,N*N):
                    # print('pirmas for veikia')
                        if (it < lastText * 4):
                            letter = imagereadDecoding.hilbert2xy(i, N, lastText, 2, it, img_resized, rgbValue[0])
                            m = it
                        # print(m)
                            if (it >= symbolsCount):
                                m = int(it%symbolsCount)
                            # print(m)
                                decodedText[m] = decodedText[m] + letter
                            else:
                                decodedText.append(letter)        
                        it = it + 1   
                
                if (textLength >= symbolsCount):    
                    for i in range(0,N*N):
                        # print('antras for veikia')
                    #print('nextvisad ', nextletter)
                        if (it1 < lastText * 4):
                        #print(it1)
                            letter = imagereadDecoding.hilbert2xy(i, N, lastText, 2, it1, img_resized, rgbValue[1])
                                #m = it1                            
                            m = it1
                            if (nextletter >= (symbolsCount*2)):                                
                                if (it1==lastText*2):
                                    it2 = it2 + lastText
                                elif (it1==lastText*3):
                                    it2 = it2 + lastText
                                m = int(nextletter - it2)
                                decodedText[m] = decodedText[m] + letter
                                # print('m2for ', m)
                            else:
                                decodedText.append(letter)
                            #print('pirma',m)       
                        it1 = it1 + 1
                        it = it + 1
                        nextletter = nextletter + 1
                if (textLength >= symbolsCount*2): 
                    for i in range(0,N*N):
                        # print('trecias for veikia')
                    #print('nextvisad ', nextletter)
                        if (it4 < lastText2 * 4):
                        #print(it1)
                            letter = imagereadDecoding.hilbert2xy(i, N, lastText2, 2, it4, img_resized, rgbValue[2])
                                #m = it1                            
                            m = it4
                            if (nextletter2 >= textLength):                                
                                if (it4==lastText2*2):
                                    it3 = it3 + lastText2
                                elif (it4==lastText2*3):
                                    it3 = it3 + lastText2
                                m = int(nextletter2 - it3)
                                # print('m ', m)
                                decodedText[m] = decodedText[m] + letter
                            else:
                                decodedText.append(letter)
                                print("teksto ilgis ", len(decodedText))
                            # print('pirma',m)       
                        it4 = it4 + 1
                        it = it + 1
                        nextletter2 = nextletter2 + 1


            text = ''
            if (decodedText != []):
                #text = ''
                for letter in decodedText:
                    text = text + chr(letter)
            self.result.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                font: 10pt "Microsoft YaHei"')
            self.result.setText("Dekoduotas tekstas: \n"+text)
            #self.textEdit.setDisabled(True)
            self.result.setVisible(True)
        else:
            self.symbols.setText("Paveisklėlis, kurį pasirinkote nerastas.\
 Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)")
            self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)
            

    def compareImage_clicked(self):
        #self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Gerai")
        #self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Uždaryti")
        imageencoded = self.imagepath.text()
        imagedecoded = "uzkoduoti/" + self.decodedname.text()
        Dialog = QtWidgets.QDialog()
        loadUi('ImageShow.ui', Dialog)
        #JEI BUS NEVIENODO DYDZIO tai reik resize padaryt kazkaip logiskai
        #Dialog.exit(app.exec_())
        pixmapEncoded = QPixmap(imageencoded)
        pixmapDecoded = QPixmap(imagedecoded)
        #print(imageencoded)
        Dialog.image1.setPixmap(QPixmap(pixmapEncoded))
        #Dialog.image1.resize(pixmapEncoded.width(), pixmapEncoded.height())
        Dialog.image2.setPixmap(QPixmap(pixmapDecoded))
        Dialog.image2.resize(pixmapDecoded.width(), pixmapDecoded.height()) 
        Dialog.resize(pixmapDecoded.width()+pixmapEncoded.width(), pixmapDecoded.height())   
        Dialog.show()
        Dialog.exec_()

    def encodeButton_clicked(self):
        imagePath = self.imagepath.text()
        if Path(imagePath).is_file():
            img = Image.open(imagePath)

            img_resized = img.load() #uzsikraunam pikselius
            [xs,ys] = img.size
            N = highestPowerof2(min(xs,ys))
            symbolsCount = N*N/4
            # /4, nes koduojam po du bitukus, 
            # tai viena baitui uzkoduoti reikia 4pikseliu
            it = 0
            it1 = 0
            it2 = 0
            text = self.textEdit.toPlainText()
            # for i in range(0,N*N):  
            #     if (it < len(text) * 4):
            #         imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized)
            #         it = it + 1

            #BANDOM SU RGB
            #symC = N*N/4 #is keturiu, nes koduojam dviejuose bitukuose
            rgbValue = str(self.RGBcomboBox.currentText())
            #print(rgbValue)
            if rgbValue == 'r' or rgbValue == 'g' or rgbValue == 'b':
                for i in range(0,N*N):  
                    if (it < len(text) * 4):
                        imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized, rgbValue)
                        it = it + 1
            elif rgbValue == 'r g' or rgbValue == 'r b' or rgbValue == 'b g':
                rgbValue = rgbValue.split(' ')  
                if (it < len(text) * 4):
                    if (len(text) <= symbolsCount):
                        for i in range(0,N*N):
                            imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized, rgbValue[0])
                            it = it + 1
                    else:
                        text1 = text[:int(symbolsCount)]
                        textLast = text[int(symbolsCount):]
                        if (len(text) > (symbolsCount*2)):
                            textLast = text[int(symbolsCount):int(symbolsCount*2)]     
                        for i in range(0,N*N):
                            imagereadEncoding.hilbert2xy(i,N, text1, 2, it, img_resized, rgbValue[0])
                            it = it + 1
                        # lastText = int(symbolsCount)
                        #print(text[lastText:])
                        for i in range(0,N*N):
                            imagereadEncoding.hilbert2xy(i,N, textLast, 2, it1, img_resized, rgbValue[1])
                            it = it + 1 
                            it1 = it1 + 1
            elif rgbValue == 'r g b':
                rgbValue = rgbValue.split(' ')  
                if (it < len(text) * 4):
                    # if (len(text) <= symbolsCount):
                    #     for i in range(0,N*N):
                    #         imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized, rgbValue[0])
                    #         it = it + 1
                    # else:
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
                        for i in range(0,N*N):
                            imagereadEncoding.hilbert2xy(i,N, text1, 2, it, img_resized, rgbValue[0])
                            it = it + 1
                        # lastText = int(symbolsCount)
                        #print(text[lastText:])
                        if (len(text) > symbolsCount):
                            for i in range(0,N*N):
                                imagereadEncoding.hilbert2xy(i,N, text2, 2, it1, img_resized, rgbValue[1])
                                it = it + 1 
                                it1 = it1 + 1
                        if (len(text) > symbolsCount*2):
                            for i in range(0,N*N):
                                imagereadEncoding.hilbert2xy(i,N, textLast, 2, it2, img_resized, rgbValue[2])
                                it = it + 1 
                                it2 = it2 + 1
                    elif (len(text) < symbolsCount):
                        for i in range(0,N*N):
                            imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized, rgbValue[0])
                            it = it + 1


            path = "uzkoduoti/"
            if not self.decodedname.text():
                decodedname = "test.png"
            else:
                decodedname = self.decodedname.text()
            img.save(path + decodedname)
            self.textEdit.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                font: 10pt "Microsoft YaHei"')
            self.textEdit.setText("Užkoduoto teksto ilgis: "+str(len(text))+
"\nUžkoduotas paveikslėlis išsaugotas uzkoduoti folderyje "+decodedname+" pavadinimu"+
"\nUžkoduotas tekstas: "+text)
            self.textEdit.setVisible(True)
            self.compareImage.setVisible(True)
        else:
            self.symbols.setText("Paveisklėlis, kurį pasirinkote nerastas.\
 Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)")
            self.symbols.setStyleSheet('color: #ff4902; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)

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

    def decodedMenu_clicked(self):
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setText("Pasirinkite norimą atkoduoti\npaveikslėlį")  
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
        self.imagename.setText("")
        self.imagename.setVisible(True)
        self.label.setVisible(True)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        self.RGBcomboBox.setVisible(True)

    def encodedMenu_clicked(self):
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setText("Pasirinkite norimą užkoduoti\npaveikslėlį")        
        self.labelImage.setVisible(True)
        self.symbols.setVisible(False)
        self.labelName.setVisible(True)
        self.decodedname.setVisible(True)
        self.compareImage.setVisible(False)
        self.textLength.setVisible(False)
        self.textEdit.setVisible(True)
        self.decode.setVisible(False)
        self.encode.setVisible(True)
        self.browse.setVisible(True)
        self.imagename.setText("")
        #self.imagename.setVisible(True)
        self.label.setVisible(False)
        self.label1.setVisible(True)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        self.RGBcomboBox.setVisible(True)
        
    def getImage(self):

      cwd = os.getcwd()
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            cwd, "Image files (*.jpg *.jpeg, *.png)")
      # print(fname[0])
      if Path(fname[0]).is_file():
        # print('aaaa')
        imagePath = fname[0]
        img = Image.open(imagePath)
        img_resized = img.load() #uzsikraunam pikselius
        [xs,ys] = img.size
        N = highestPowerof2(min(xs,ys))
        symbolsCount = N*N/4*3
        imageName = imagePath.split("/")[-1]
        self.imagename.setText(imageName)
        self.imagepath.setText(imagePath)
        if (self.labelImage.text()=="Pasirinkite norimą užkoduoti\npaveikslėlį"):
            self.symbols.setText('Maksimalus simbolių skaičius, kurį galite užkoduoti \
yra '+str(int(symbolsCount))+', \njeigu pasirinksite kodavimą visose trijose rgb kodo \
koordinatėse')
            self.symbols.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
            self.symbols.setVisible(True)
      

app = QtWidgets.QApplication(sys.argv)
gui = Window()
gui.show()
sys.exit(app.exec_())
