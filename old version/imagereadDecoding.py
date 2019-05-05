from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import numpy as np
import os
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import colorsys
from PIL import Image
import sys
class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        loadUi('gui.ui',self)
        self.setWindowTitle('Erdvę užpildančios kreivės')
        self.decode.clicked.connect(self.decodeButton_clicked)
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
            letter = hilbert2xy(i, N, textLength, 2, it, img_resized)          
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
        self.label2.setText(text)
    def getImage(self):
      fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file',
                            'c:\\', "Image files (*.jpg *.jpeg, *.png)")
      imagePath = fname[0]
      imageName = imagePath.split("/")[-1]
      #pixmap = QPixmap(imagePath)
      #self.label2.setPixmap(QPixmap(pixmap))
      self.imagename.setText(imageName)
      self.imagepath.setText(imagePath)
      #self.resize(pixmap.width(), pixmap.height())
#tk.Spinbox()


def getSum(a, b):
    while b:
        a, b = (a ^ b), (a & b) << 1
    return a

# (2) Get image width & height in pixels
#[xs, ys] = img.size    

#check if the color is not out of limit
#def clamp(x): 
#  return max(0, min(x, 255))

#encoding function

def decoding(b, it, bits, textLength):
  #textLength = int(sys.argv[2])

  #kol kart 4, nes darom kad keiciam po du bitukus ir tada turim kiekvienai
  #raidei/char 4 poras.
  bb = (b & 3)
  if (it < textLength*4):
      if (it < textLength):        
        bb = bb << 6
      elif (textLength <= it < textLength*2):
        bb = bb << 4
            #print(bin(letter))
            #print(bin(48))
      elif (textLength*2 <= it < textLength*3):
        bb = bb << 2
            #print(bin(letter))
      elif (textLength*3 <= it < textLength*4):
        bb = bb
  return(bb)
      


#nuskaityti kaip hilberto seka
        
def last2bits(hindex):
  return (hindex & 3)
def rshift(val, n): return (val % 0x100000000) >> n
def hilbert2xy(hindex, N, textLength, bits, it, img_resized):
  positions = [
    [0, 0],
    [0, 1],
    [1, 1],
    [1, 0]
  ]
  
  tmp = positions[last2bits(hindex)]
  hindex = rshift(hindex, 2)
  x = tmp[0]
  y = tmp[1]
  for n in range(4, N+1):
    if (n & (n-1) == 0) :    
      n2 = n/2
      if (last2bits(hindex) == 0):
        tmp = x
        x = y
        y = tmp
      elif (last2bits(hindex) == 1):
        x = x
        y = y + n2
      elif (last2bits(hindex) == 2):
        x = x + n2
        y = y + n2
      elif (last2bits(hindex) == 3):
        tmp = y
        y = (n2 - 1) - x
        x = (n2 - 1) - tmp
        x = x + n2

      hindex = rshift(hindex, 2)
  #print(x,y)
  [r, g, b] = img_resized[x, y]
  letter = decoding(b, it, bits, textLength)
  return (letter)
  #print(img_resized[x,y])
  
      
    


 #turi buti argv
#print(textLength)
#it = 0
app = QtWidgets.QApplication(sys.argv)
gui = Window()
gui.show()
sys.exit(app.exec_())
#for i in range(0,N*N): 
      #ir dar vietoj texto padavineti teksto ilgi, kuri gausim is parametru      
#  if (it < textLength * 4):
#    letter = hilbert2xy(i,N, textLength, 2, it)          
#    m = it          
    #print(decodedText)
 #   if (it >= textLength):
  #    m = it%textLength
   #   decodedText[m] = decodedText[m] + letter
    #else:
     # decodedText.append(letter)        
  #it = it + 1
  
#if (decodedText != []):
 #   text = ''
  #  for letter in decodedText:
   #     text = text + chr(letter)
    #print(text)
    #print(decodedText)
#img.save("test.png")
