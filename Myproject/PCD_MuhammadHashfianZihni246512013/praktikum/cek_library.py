import sys
import cv2, numpy, matplotlib
import PIL, scipy
from PyQt6.QtCore import PYQT_VERSION_STR

print("Python    :", sys.version.split()[0])
print("OpenCV    :", cv2.__version__)
print("NumPy     :", numpy.__version__)
print("Matplotlib:", matplotlib.__version__)
print("Pillow    :", PIL.__version__)
print("SciPy     :", scipy.__version__)
print("PyQt6     :", PYQT_VERSION_STR)
