import imagereadDecoding
import numpy as np
import os
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
#225891
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
    @pyqtSlot()
    
    def decodeButton_clicked(self):
        
        textLength = self.textLength.value()
        imagePath = self.imagepath.text()
        img_file = Image.open(imagePath)

        img = img_file.resize((256, 256), Image.ANTIALIAS)

        img_resized = img.load() #uzsikraunam pikselius
        N = 256
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

    def compareImage_clicked(self):
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
        img_file = Image.open(imagePath)

        img = img_file.resize((256, 256), Image.ANTIALIAS)

        img_resized = img.load() #uzsikraunam pikselius
        N = 256
        it = 0
        text = self.textEdit.toPlainText()
        for i in range(0,N*N):  
          if (it < len(text) * 4):
            imagereadEncoding.hilbert2xy(i,N, text, 2, it, img_resized)
            it = it + 1
        path = "uzkoduoti/"
        decodedname = self.decodedname.text()
        img.save(path + decodedname)
        self.result.setStyleSheet('color: yellow; background-color: rgba(0,0,0,0%)')
        self.result.setText("Užkoduoto teksto ilgis: "+str(len(text)))
        self.result.setVisible(True)
        self.compareImage.setVisible(True)

    def about_clicked(self):
        self.labelImage.setVisible(False)
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

    def decodedMenu_clicked(self):
        self.labelImage.setVisible(True)
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

    def encodedMenu_clicked(self):
        self.labelImage.setText("Pasirinkite norimą užkoduoti\npaveikslėlį")
        self.labelImage.setStyleSheet('color: white; background-color: rgba(0,0,0,0%);\
            font: 10pt "Microsoft YaHei"')
        self.labelImage.setVisible(True)
        self.labelName.setVisible(True)
        self.decodedname.setVisible(True)
        self.compareImage.setVisible(False)
        self.textLength.setVisible(False)
        self.textEdit.setVisible(True)
        self.decode.setVisible(False)
        self.encode.setVisible(True)
        self.browse.setVisible(True)
        self.imagename.setVisible(True)
        self.label.setVisible(False)
        self.label1.setVisible(True)
        self.result.setVisible(False)
        self.aboutBrowser.setVisible(False)
        
    def getImage(self):
      cwd = os.getcwd()
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            cwd, "Image files (*.jpg *.jpeg, *.png)")
      imagePath = fname[0]
      imageName = imagePath.split("/")[-1]
      self.imagename.setText(imageName)
      self.imagepath.setText(imagePath)
      

app = QtWidgets.QApplication(sys.argv)
gui = Window()
gui.show()
sys.exit(app.exec_())
