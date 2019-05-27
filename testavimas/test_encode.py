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
import EncodingFile
import DecodingFile
import unittest
import about
import QTest


def test_file_exist():
	assert about.gui.labelImage.text() == "Pasirinkite norimą užkoduoti paveikslėlį"