import colorsys
from PIL import Image
import sys
import os
from pathlib import Path
import EncodingFile
import DecodingFile
import imageEncoding
import imageDecoding
from main import Window
from main import decodedCycle, decodeFile, encodeFile, highestPowerof2
from PyQt5.QtCore import *
  
# --------------------------------------TESTING TEXT FROM INPUT----------------------------------------------------

def codeText(qtbot, text, rgbValue, bits, decodedImage):
	window = Window()
	qtbot.addWidget(window)
	window.imagename.setText("18.jpg")
	window.textEdit.setText(text)
	text = window.textEdit.toPlainText()
	index = window.RGBcomboBox.findText(rgbValue, Qt.MatchFixedString)
	window.RGBcomboBox.setCurrentIndex(index)
	index1 = window.bitsComboBox.findText(bits, Qt.MatchFixedString)
	window.bitsComboBox.setCurrentIndex(index1)
	window.decodedname.setText(decodedImage)
	qtbot.mouseClick(window.encode, Qt.LeftButton)
	#decoding
	window.imagename.setText(decodedImage)
	window.imagepath.setText(decodedImage)
	window.textLength.setValue(len(text))
	textLength = window.textLength.value()
	qtbot.mouseClick(window.decode, Qt.LeftButton)
	decodedText = window.result.toPlainText()
	return decodedText

def codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, filesize):
	window = Window()
	qtbot.addWidget(window)
	window.imagename.setText("18.jpg")
	index = window.RGBcomboBox.findText(rgbValue, Qt.MatchFixedString)
	window.RGBcomboBox.setCurrentIndex(index)
	index1 = window.bitsComboBox.findText(bits, Qt.MatchFixedString)
	window.bitsComboBox.setCurrentIndex(index1)
	window.decodedname.setText(decodedImage)
	window.radioButtonFile.setChecked(True)
	window.filePath.setText(txtFile)
	window.encodeFileName.setText(txtFile)
	qtbot.mouseClick(window.encode, Qt.LeftButton)
	#decoding
	window.imagename.setText(decodedImage)
	window.imagepath.setText(decodedImage)
	window.textLength.setValue(filesize)
	textLength = window.textLength.value()
	window.dradioButtonFile.setChecked(True)
	window.resultFileName.setText(txtResult)
	qtbot.mouseClick(window.decode, Qt.LeftButton)
	symbols = window.symbols.text()
	f = open(txtResult, "r")
	text = f.read()	
	return text

# First three test for one rgb color and different bits coding. len(text) < Symmbols Count
def test_textR2_5(qtbot):
	text = 'labas'
	rgbValue = 'r'
	bits = '2'
	decodedImage = "uzkoduoti/input/r2_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

def test_textR4_5(qtbot):
	text = 'labas'
	rgbValue = 'r'
	bits = '4'
	decodedImage = "uzkoduoti/input/r4_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

def test_textR8_5(qtbot):
	text = 'labas'
	rgbValue = 'r'
	bits = '8'
	decodedImage = "uzkoduoti/input/r8_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"


# Next three test for one rgb color and different bits coding. len(text) > Symmbols Count
def test_textR2_17(qtbot):
	text = 'labas labas labas'
	rgbValue = 'r'
	bits = '2'
	decodedImage = "uzkoduoti/input/r2_17.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas laba"

def test_textR4_35(qtbot):
	text = "labas labas labas labas labas labas"
	rgbValue = 'r'
	bits = '4'
	decodedImage = "uzkoduoti/input/r4_35.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas la"

def test_textR8_71(qtbot):
	text = "labas labas labas labas labas labas labas labas labas labas labas labas"
	rgbValue = 'r'
	bits = '8'
	decodedImage = "uzkoduoti/input/r8_71.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas labas labas laba"

# Next three test for two rgb color and different bits coding. len(text) < Symmbols Count
def test_textRB2_5(qtbot):
	text = "labas"
	rgbValue = 'r b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rb2_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

def test_textRB4_5(qtbot):
	text = "labas"
	rgbValue = 'r b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rb4_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

def test_textRB8_5(qtbot):
	text = "labas"
	rgbValue = 'r b'
	bits = '8'
	decodedImage = "uzkoduoti/input/rb8_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

# Next three test for two rgb color and different bits coding. Symbols Count < len(text) < Symmbols Count * 2
def test_textRB2_17(qtbot):
	text = "labas labas labas"
	rgbValue = 'r b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rb2_17.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas"

def test_textRB4_47(qtbot):
	text = "labas labas labas labas labas labas labas labas"
	rgbValue = 'r b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rb4_47.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas"

def test_textRB8_95(qtbot):
	text = "labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas"
	rgbValue = 'r b'
	bits = '8'
	decodedImage = "uzkoduoti/input/rb8_95.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas"

# Next two test for two rgb color and different bits coding. len(text) > Symmbols Count * 2
def test_textRB2_41(qtbot):
	text = "labas labas labas labas labas la"
	rgbValue = 'r b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rb2_41.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas la"

def test_textRB4_41(qtbot):
	text = "labas labas labas labas labas lalabas labas labas labas labas la"
	rgbValue = 'r b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rb2_64.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas lalabas labas labas labas labas la"

# Next three test for three rgb color and different bits coding. len(text) < Symmbols Count
def test_textRGB2_5(qtbot):
	text = "labas"
	rgbValue = 'r g b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rgb2_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas" 

def test_textRGB4_5(qtbot):
	text = "labas"
	rgbValue = 'r g b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rgb4_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

def test_textRGB8_5(qtbot):
	text = "labas"
	rgbValue = 'r g b'
	bits = '8'
	decodedImage = "uzkoduoti/input/rgb8_5.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas"

# Next three test for three rgb color and different bits coding. Symbols Count < len(text) < Symmbols Count * 2
def test_textRGB2_17(qtbot):
	text = "labas labas labas"
	rgbValue = 'r g b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rgb2_17.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas"

def test_textRGB4_35(qtbot):
	text = "labas labas labas labas labas labas"
	rgbValue = 'r g b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rgb4_35.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas"

def test_textRGB8_71(qtbot):
	text = "labas labas labas labas labas labas labas labas labas labas labas labas"
	rgbValue = 'r g b'
	bits = '8'
	decodedImage = "uzkoduoti/input/rgb8_71.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas labas labas labas labas"

# Next three test for three rgb color and different bits coding. Symbols Count * 2  < len(text) < Symmbols Count * 3
def test_textRGB2_35(qtbot):
	text = "labas labas labas labas labas labas"
	rgbValue = 'r g b'
	bits = '2'
	decodedImage = "uzkoduoti/input/rgb2_35.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas"

def test_textRGB4_71(qtbot):
	text = "labas labas labas labas labas labas labas labas labas labas labas labas"
	rgbValue = 'r g b'
	bits = '4'
	decodedImage = "uzkoduoti/input/rgb4_71.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas labas labas labas labas"

def test_textRGB8_142(qtbot):
	text = "labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas"
	rgbValue = 'r g b'
	bits = '8'
	decodedImage = "uzkoduoti/input/rgb8_142.png"
	decodedText = codeText(qtbot, text, rgbValue, bits, decodedImage)
	assert decodedText == "Dekoduotas tekstas: \nlabas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas labas"


# ---------------------------TESTING FILE-------------------------------------------------

def test_fileB2_5(qtbot):
	rgbValue = 'b'
	txtFile = "txt/5.txt"
	txtResult = "result/1.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/b2_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileB4_5(qtbot):
	rgbValue = 'b'
	txtFile = "txt/5.txt"
	txtResult = "result/2.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/b4_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileB8_5(qtbot):
	rgbValue = 'b'
	txtFile = "txt/5.txt"
	txtResult = "result/3.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/b8_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB2_5(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/5.txt"
	txtResult = "result/4.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/rb2_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB4_5(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/5.txt"
	txtResult = "result/5.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/rb4_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB8_5(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/5.txt"
	txtResult = "result/6.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/rb8_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB2_17(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/17.txt"
	txtResult = "result/7.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/rb2_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 17)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB4_35(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/35.txt"
	txtResult = "result/8.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/rb4_35.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 35)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRB8_71(qtbot):
	rgbValue = 'r b'
	txtFile = "txt/71.txt"
	txtResult = "result/9.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/rb8_71.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 71)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB2_5(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/5.txt"
	txtResult = "result/9.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/rgb2_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB4_5(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/5.txt"
	txtResult = "result/10.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/rgb4_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB8_5(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/5.txt"
	txtResult = "result/11.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/rgb8_5.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 5)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB2_17(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/17.txt"
	txtResult = "result/12.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/rgb2_17.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 17)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB4_35(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/35.txt"
	txtResult = "result/13.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/rgb4_35.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 35)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB8_71(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/71.txt"
	txtResult = "result/14.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/rgb8_71.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 71)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB2_35(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/35.txt"
	txtResult = "result/15.txt"
	bits = '2'
	decodedImage = "uzkoduoti/failai/rgb2_35.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 35)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB4_71(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/71.txt"
	txtResult = "result/16.txt"
	bits = '4'
	decodedImage = "uzkoduoti/failai/rgb4_71.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 71)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1

def test_fileRGB8_143(qtbot):
	rgbValue = 'r g b'
	txtFile = "txt/143.txt"
	txtResult = "result/17.txt"
	bits = '8'
	decodedImage = "uzkoduoti/failai/rgb8_143.png"
	text = codeFile(qtbot, rgbValue, bits, decodedImage, txtFile, txtResult, 143)
	f = open(txtFile, "r")
	text1 = f.read()
	assert text == text1