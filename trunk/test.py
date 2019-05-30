import sys
import unittest
from PyQt5.QtCore import *

from main import Window

def test_basic_search(qtbot):
	window = main.Window()
	window.show()
	qtbot.addWidget(window)
	qtbot.mouseClick(window.encodedMenu, QtCore.Qt.LeftButton)
	qtbot.mouseClick(window.encode, QtCore.Qt.LeftButton)
	assert window.symbols.text() == "Paveikslėlis, kurį pasirinkote nerastas.Pažiūrėkite, \nar nurodėte tikslią paveikslėlio vietą (tikslų kelią iki jo)"
 	sys.exit()
