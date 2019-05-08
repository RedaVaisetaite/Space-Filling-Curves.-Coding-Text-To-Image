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
            decodedText = []
            it = 0
            for i in range(0,N*N): 
        #ir dar vietoj texto padavineti teksto ilgi, kuri gausim is parametru      
                if (it < textLength * 4):
                    letter = imagereadDecoding.hilbert2xy(i, N, textLength, 2, it, img_resized)          
                    m = it          
      #print(decodedText)
                    if (it >= textLength):
                        m = it%textLength
                        decodedText[m] = decodedText[m] + letter
                    else:
                        decodedText.append(letter)        
                it = it + 1
  
            if (decodedText != []):
                text = ''
                for letter in decodedText:
                    text = text + chr(letter)
            self.textEdit.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%);\
                font: 10pt "Microsoft YaHei"')
            self.textEdit.setText("Dekoduotas tekstas: \n"+text)
            self.textEdit.setDisabled(True)
            self.textEdit.setVisible(True)
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
        Dialog.show()
        Dialog.exec_()

    def encodeButton_clicked(self):
        imagePath = self.imagepath.text()
        if Path(imagePath).is_file():
            img = Image.open(imagePath)

            img_resized = img.load() #uzsikraunam pikselius
            [xs,ys] = img.size
            N = highestPowerof2(min(xs,ys))
            symbolsCount = N*N/4*3 #*3 nes turim r,g,b; /4, nes koduojam po du bitukus, 
            # tai viena baitui uzkoduoti reikia 4pikseliu
            it = 0
            text = self.textEdit.toPlainText()
            for i in range(0,N*N):  
                if (it < len(text) * 4):
                    imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized)
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
        self.RGBcomboBox.setVisible(False)

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
