import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import colorsys
from PIL import Image
import tkinter as tk

#tk.Spinbox()
#img_file = Image.open("theview.jpg")
img_file = Image.open("test.png")

img = img_file.resize((256, 256), Image.ANTIALIAS)

img_resized = img.load() #uzsikraunam pikselius

def getSum(a, b):
    while b:
        a, b = (a ^ b), (a & b) << 1
    return a

# (2) Get image width & height in pixels
[xs, ys] = img.size    

#check if the color is not out of limit
#def clamp(x): 
#  return max(0, min(x, 255))

#encoding function
def encoding(intText, b, it, bits):
  #kol kart 4, nes darom kad keiciam po du bitukus ir tada turim kiekvienai
  #raidei/char 4 poras.
  if (it < len(intText)*4):
      m = it
      if (it >= len(intText)):
          m = it%len(intText)
      #dabar darau tik su dviejais bitais. bet jei reiktu su n bitu, tai
      #tada darytume taip:
      #and'int su 2**n-1 raides bitais ir 255-2**n-1 su spalvos bitais
      bReplaced = b & 255-(2**bits-1)
      if (it < len(intText)):
        intText[m] = (intText[m] & 192)
        intText[m] = intText[m] >> 6
        
            #print(intText[letter])
      elif (len(intText) <= it < len(intText)*2):
        intText[m] = (intText[m] & 48)
        intText[m] = intText[m] >> 4
            #print(bin(letter))
            #print(bin(48))
      elif (len(intText)*2 <= it < len(intText)*3):
        intText[m] = (intText[m] & 12)
        intText[m] = intText[m] >> 2
            #print(bin(letter))
      elif (len(intText)*3 <= it < len(intText)*4):
        intText[m] = (intText[m] & 3)
      
      b = getSum(bReplaced, intText[m])
  return(b)

def decoding(b, it, bits, textLength):
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
m = 0
def hilbert2xy(hindex, N, text, bits, it, encode):
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
  intText = [int(format(ord(x), '08b'), 2) for x in text]
  if (encode == 'e'):
      b = encoding(intText, b, it, bits)
      img_resized[x,y] = r,g,b
      
      return(x,y)
  if (encode == 'd'):
      letter = decoding(b, it, bits, len(text))
      return (letter)
  #print(img_resized[x,y])
  
      
    

N = 256
decodedText = []
code = 'd'
text = "?!,ToksTas gyvenimas kai tau astuoneri suejo"
textLength = len(text)
#print(textLength)
it = 0
for i in range(0,N*N):  
  if (code == 'd'):
      #ir dar vietoj texto padavineti teksto ilgi, kuri gausim is parametru      
      if (it < textLength * 4):
          letter = hilbert2xy(i,N, text, 2, it, 'd')
          
          m = it          
          #print(decodedText)
          if (it >= textLength):
              m = it%textLength
              decodedText[m] = decodedText[m] + letter
          else:
              decodedText.append(letter)
              
          #print(m)          
  elif (code == 'e'):
      hilbert2xy(i,N, text, 2, it, 'e')
  it = it + 1
if (decodedText != []):
    text = ''
    for letter in decodedText:
        text = text + chr(letter)
    print(text)
    #print(decodedText)
#img.save("test.png")
