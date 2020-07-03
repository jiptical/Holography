#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:06:56 2020

@author: parker
"""

# -*- coding: utf-8 -*-
"""
Demonstrates a variety of uses for ROI. This class provides a user-adjustable
region of interest marker. It is possible to customize the layout and 
function of the scale/rotate handles in very flexible ways. 
"""

"""
You will need to have the following packages installed:
    
    pyqtgraph     http://www.pyqtgraph.org
    PyQt
    PIL
    Numpy
    
"""


# PYQYGRAPH 
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


# Image Wrangler
import numpy as np
from PIL import Image as im

#Dependencies required for 3D Plotting 
from pyqtgraph.widgets import MatplotlibWidget as mpw
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Fix for using pyqtgraph
pg.setConfigOptions(imageAxisOrder='row-major')


# create GUI
app = QtGui.QApplication([])
W = QtGui.QWidget()
w = pg.GraphicsWindow( border=True)
w.setWindowTitle('Image Data Tools')

# Set layout to display each part in a grid
layout = QtGui.QGridLayout()
W.setLayout(layout)

text = """Data Selection From Image.<br>\n
Drag to update the selected image.
Hold CTRL while dragging for fine control.
"""
btn = QtGui.QPushButton('Update 3D')

#Image wrangler
pic = im.open('BB12_Ep.bmp')
arr = np.array(pic)
arr = arr[:,:]

w1 = w.addLayout(row=0, col=0)
label1 = w1.addLabel(text, row=0, col=0)

viewer = w1.addViewBox(row=1, col=0, colspan=1, lockAspect=True)
viewer.setMaximumHeight(400)
viewer.setMaximumWidth(800)
p1 = w1.addPlot(row=2, col=0, lockAspect=True)
p1.setMaximumHeight(400)
p1.setMaximumWidth(400)
img1a = pg.ImageItem(arr)
viewer.addItem(img1a)
img1b = pg.ImageItem()
p1.addItem(img1b)
# viewer.disableAutoRange('xy')
# p1.disableAutoRange('xy')
viewer.autoRange()
p1.autoRange()
# p2 = w1.addPlot(row=3, col=0)


# Create image to display


mw = mpw.MatplotlibWidget(size=[10,8])
ax = mw.getFigure().add_subplot(111,projection='3d')

def surface_plot (matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    ax.cla()
    ax.clear()
    (x, y) = np.meshgrid(np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (surf)


Z = arr[0:500,0:500]
surf = surface_plot(Z, cmap='coolwarm')




layout.addWidget(w,0,0,3,3)
layout.addWidget(mw,0,4,3,6)
layout.addWidget(btn,0,1)
W.show()

# ROI's for whole image
rois = []
rois.append(pg.RectROI([100, 100], [200, 200], pen=(0,9),resizable=False))





# Updater for primary ROI's
def update(roi):
    selection = roi.getArrayRegion(arr, img1a)
    img1b.setImage(selection, levels=(0, arr.max()))
    # (ax,surf) = surface_plot(selection,cmap=plt.cm.coolwarm)
    p1.autoRange()
    

for roi in rois:
    roi.sigRegionChanged.connect(update)
    viewer.addItem(roi)
    update(rois[-1])


def update3D():
    selection = roi.getArrayRegion(arr, img1a)
    surface_plot(selection,cmap='coolwarm')
    mw.draw()
    
btn.clicked.connect(update3D)




# Updater for Secondary ROI
# def updatePlot():
#     global p1, subroi, arr, p2, selected
#     selected = subroi.getArrayRegion(arr, img1b)
#     p2.plot(selected.mean(axis=0), clear=True)
#     p2.autoRange()
   


# subroi.sigRegionChanged.connect(updatePlot)
# updatePlot()



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()