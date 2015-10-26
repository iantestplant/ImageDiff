#
#Compare Images tool
#
# author: Ian Parker
# Copyright (C) 2015	TestPlant UK Ltd


import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QSettings, QPoint, QSize, SIGNAL, SLOT
from PyQt4.QtGui import QApplication, QMainWindow, QPixmap, QIcon, qRed, qGreen, qBlue, qAlpha
import ImageDiff_rc

from ui.Ui_mainWindow import Ui_MainWindow
title = u"eggPlant Image Differencing"
version = "0.2"

class node(QtGui.QGraphicsPixmapItem):
	def __init__(self, path, mw):
		self.mw = mw
		self.path = path
		QtGui.QGraphicsPixmapItem.__init__(self, QPixmap(path))
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
		self.setFlag(self.ItemIsFocusable, True)
		self.showOverlay()

	def focusInEvent(self, e):
		self.mw.scene.prevFocus = self

	def mousePressEvent(self, e):
		if e.button() == QtCore.Qt.LeftButton:
			self.setOpacity(0.5)
		QtGui.QGraphicsPixmapItem.mousePressEvent(self, e)

	def mouseReleaseEvent(self, e):
		if e.button() == QtCore.Qt.LeftButton:
			self.setOpacity(1)
			self.showOverlay()
		QtGui.QGraphicsPixmapItem.mouseReleaseEvent(self, e)

	def contextMenuEvent(self, event):
		self.setFocus()
		self.menu = QtGui.QMenu()
		if self.collidingItems():
			actionStackBefore = self.menu.addAction(renameIcon16, "Send behind ovelapping image")
			actionStackBefore.triggered.connect(self.pushBefore)
		actionRemove = self.menu.addAction(deleteIcon16, "Remove Image")
		actionRemove.triggered.connect(self.removeAction)

		self.menu.exec_(event.screenPos())
		event.setAccepted(True)

	def removeAction(self):
		QApplication.postEvent(self.mw, QtCore.QEvent(2113))

	def pushBefore(self):
		items = self.collidingItems()
		if items:
			self.stackBefore(items[0])
			self.clearFocus()
			items[0].setFocus()
			self.update()
			items[0].update()

	def showOverlay(self):
		items = self.collidingItems()
		if items:
			# get intersection as a RectF in scene coodinates
			rect_intersect = self.sceneBoundingRect().intersected(items[0].sceneBoundingRect())

			# map scene intersect to a QPolygonF foreach GraphicsItem that can be used to get the overlapping area of each item
			qpoly = self.mapFromScene(rect_intersect)
			qpoly1 = items[0].mapFromScene(rect_intersect)

			# Create new pixmaps containing just the overlapped regions.
			# This seems to be +/- 1 pixel so perhaps needs refining.
			p1 = self.pixmap().copy(qpoly.boundingRect().toRect() )
			p2 = items[0].pixmap().copy(qpoly1.boundingRect().toRect() )
			self.mw.pm1 = p1
			self.mw.pm2 = p2
			self.mw.ui.image1_title_te.setText(self.path)
			self.mw.ui.image2_title_te.setText(items[0].path)

			i1 = p1.toImage()
			i2 = p2.toImage()
			inv = p1.toImage()
			inv.invertPixels()
			# Create a qimage to contain the matched pixes and inverted pixes where they dont match
			i3 = QtGui.QImage(p1.width(), p1.height(), QtGui.QImage.Format_RGB32)
			disc = 0 # discrepency count
			# intersect pixmaps can be different by 1 pixel
			width = min(p1.width(), p2.width())
			height = min(p1.height(), p2.height())

			rgbTolerances = self.mw.getTolerance()
			for x in range(width):
				for y in range(height):
					if self.toleranceMatch(i1.pixel(x,y), i2.pixel(x,y), rgbTolerances):
						i3.setPixel(x, y, i1.pixel(x,y)) # copy the pixel
					else:
						i3.setPixel(x, y, inv.pixel(x,y)) # copy the inverse pixel
						disc +=1

			self.mw.pm3 = QtGui.QPixmap.fromImage(i3)
			self.mw.ui.compare_title_te.setText("discrepency %d%% %d pixels"%( 100 * disc/(width * height), disc))

			self.mw.showImages()
		else:
			self.mw.ui.image2_lbl.clear()
			self.mw.ui.overlay_lbl.clear()

	def toleranceMatch(self, px1, px2, rgbTolerances):
		if (abs(qRed(px1) - qRed(px2))) > rgbTolerances[0] or (abs(qGreen(px1) - qGreen(px2))) > rgbTolerances[1] or (abs(qBlue(px1) - qBlue(px2))) > rgbTolerances[2]:
			return False
		if not self.mw.ui.actionIgnore_Transparent_Pixels.isChecked():
			return abs(qAlpha(px1) == qAlpha(px2))
		return True

	def mouseMoveEvent(self, event):
		#self.showOverlay() # too slow!
		QtGui.QGraphicsPixmapItem.mouseMoveEvent(self, event)

	def keyPressEvent(self, e):
		x_offset = y_offset = 1
		if e.key() == QtCore.Qt.Key_Right:
			self.setPos(self.x()+x_offset, self.y())
		elif e.key() == QtCore.Qt.Key_Left:
			self.setPos(self.x()-x_offset, self.y())
		elif e.key() == QtCore.Qt.Key_Down:
			self.setPos(self.x(), self.y()+y_offset)
		elif e.key() == QtCore.Qt.Key_Up:
			self.setPos(self.x(), self.y()-y_offset)
		self.showOverlay()


class Scene(QtGui.QGraphicsScene):
	nodes = []

	def __init__(self, parent):
		self.parent = parent
		QtGui.QGraphicsScene.__init__(self)

		self.prevFocus = None

	def dragMoveEvent(self, e):
		 e.acceptProposedAction()

	def dragEnterEvent(self, e):
		 e.acceptProposedAction()

	def dropEvent(self, e):
		if e.mimeData().hasUrls():
			self.addUrls(e.mimeData().urls())
		e.acceptProposedAction()

	def contextMenuEvent(self, event):
		QtGui.QGraphicsScene.contextMenuEvent(self, event) # passes it on to the node

	def addUrls(self, urls):
		self.addImageFiles(map(lambda url: url.toLocalFile().toLocal8Bit().data(), urls))

	def addImageFiles(self, files):
		# sort so stack order in in file size with largest at the back
		n = None
		exisitingPaths =  map(lambda n: n.path, self.nodes)
		for path in sorted(files, key = lambda f: os.stat(f).st_size, reverse=True):
			if path not in exisitingPaths:
				n = node(path, self.parent)
				self.addNode(n)

		if n:
			n.setFocus()
			n.showOverlay()

	def addNode(self, n):
		self.nodes.append(n)
		self.addItem(n)

	def removeNode(self):
		n = self.focusItem()
		if n:
			self.removeItem(n)
			self.nodes.remove(n)

	def clear(self):
		for node in self.nodes:
			self.removeItem(node)
		self.nodes = []

	def showOverlay(self):
		n = self.focusItem()
		if n:
			n.showOverlay()
			self.prevFocus = n # save on case loses focus such as when changing an option
		elif self.prevFocus:
			self.prevFocus.showOverlay()

class ImageDiff(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)

		self.setWindowIcon(QIcon(":/images/ImageDiff-64.png"))

		self.imageFolder = ""
		self.pm1 = self.pm2 = self.pm3 = None

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowTitle(title)

		self.settings = QSettings("TestPlant", "imageDiff")
		self.readSettings()
		self.ui.splitter.setChildrenCollapsible(False)

		self.scene = Scene(self)
		self.ui.graphicsView.setScene(self.scene)
		self.installEventFilter(self)

		self.ui.actionClearImages.setIcon(deleteIcon16)
		self.ui.actionOpenImages.setIcon(addIcon16)
		self.ui.actionClearImages.triggered.connect(self.clearImages)
		self.ui.actionOpenImages.triggered.connect(self.openFiles)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.actionUser_Guide.triggered.connect(self.usage)
		self.ui.actionIgnore_Transparent_Pixels.triggered.connect(self.showOverlay)

		self.ui.actionExit.triggered.connect(self.close)
		self.connect(self.ui.scale_Slider, QtCore.SIGNAL("valueChanged(int)"), self.showImages)
		#self.connect(self.ui.tolerance_le, QtCore.SIGNAL("textChanged(QString)"), self.setTolerance)
		self.ui.image1_title_te.setStyleSheet("background-color: transparent;")
		self.ui.image2_title_te.setStyleSheet("background-color: transparent;")
		self.ui.compare_title_te.setStyleSheet("background-color: transparent;")

	def about(self):
		QtGui.QMessageBox.about(self, title, "%s by TestPlant\nVersion %s"%(title, version))

	def usage(self):
		QtGui.QMessageBox.about(self, "Usage", "Add files from the file menu, or by drag and drop.\n\n" +
		"Move images using the mouse or the keyboard cursor keys.\n\n" +
		"The overlapping regions of two images are shown in the lower windows.\n\n" +
		"The discrepancy is the percentage and count of different pixels.\n\n" +
		"Tolerance is the maximum allowed difference in each RGB value of a pixel.\nSet one integer for all colors or 3 for red green and blue.\n\n" +
		"Ignoring transparency is set in the options menu.\n\n"
		"Right-click an image to change overlap order or remove.")

	def getTolerance(self):
		try:
			s =  str(self.ui.tolerance_le.text())
			if not s: return (0,0,0)
			tolerances = map(lambda t: int(t), s.split())
			if len(tolerances) == 1:
				return (tolerances[0], tolerances[0], tolerances[0])
			elif len(tolerances) != 3:
				raise
		except:
			QtGui.QMessageBox.warning(self, title, "Tolerance must be an integer or 3 space separated integers for RGB")
			tolerances = (0,0,0)
		return tolerances

	def showOverlay(self):
		self.scene.showOverlay()

	def clearImages(self):
		self.scene.clear()
		self.ui.image1_lbl.clear()
		self.ui.image2_lbl.clear()
		self.ui.overlay_lbl.clear()
		self.pm1 = self.pm2 = self.pm3 = None
		self.ui.image1_title_te.clear()
		self.ui.image2_title_te.clear()
		self.ui.compare_title_te.clear()

	def showImages(self):
		self.scaleImage(self.ui.image1_lbl, self.pm1)
		self.scaleImage(self.ui.image2_lbl, self.pm2)
		self.scaleImage(self.ui.overlay_lbl, self.pm3)

	def scaleImage(self, lbl, pm):
		if pm:
			lbl.setPixmap(pm.scaled(pm.width() * self.ui.scale_Slider.value(),
			pm.height() * self.ui.scale_Slider.value(), QtCore.Qt.KeepAspectRatio))

	def openFiles(self):
		filePaths = QtGui.QFileDialog.getOpenFileNames(self, "Select images", self.imageFolder, 'image files (*.png *.tiff *.bmp);;*.*')
		if filePaths:
			self.scene.addImageFiles(filePaths)
			self.imageFolder = os.path.dirname(unicode(filePaths[0]))

	def eventFilter(self, object, event):
		if event.type() == 2113:
			self.scene.removeNode()
			return True
		return False

	def closeEvent(self, e):
		self.saveSettings()
		e.accept()

	def saveSettings(self):
		self.settings.setValue('imageFolder', self.imageFolder)
		self.settings.setValue('ignoreAlpha', self.ui.actionIgnore_Transparent_Pixels.isChecked())
		self.settings.setValue('tolerance', self.ui.tolerance_le.text())
		self.settings.beginGroup("/geometry")
		self.settings.setValue("X", self.pos().x())
		self.settings.setValue("Y", self.pos().y())
		self.settings.setValue("W", self.size().width())
		self.settings.setValue("H", self.size().height())
		self.settings.endGroup()

	def readSettings(self):
		self.imageFolder = os.path.normpath(str(self.settings.value("imageFolder").toString()))
		self.ui.actionIgnore_Transparent_Pixels.setChecked( self.settings.value("ignoreAlpha", True).toBool())
		self.ui.tolerance_le.setText( self.settings.value("tolerance").toString())
		self.settings.beginGroup("/geometry")
		p = QPoint()  # position
		s = QSize()  # size

		x = self.settings.value("X", -1).toInt()[0]
		y = self.settings.value("Y", -1).toInt()[0]
		# don't position outside current screen
		qRect = QtGui.QDesktopWidget.availableGeometry(app.desktop())
		if x > qRect.right():
			x = 10
		if y > qRect.bottom():
			y = 10
		p.setX(x)
		p.setY(y)
		s.setWidth(self.settings.value("W", -1).toInt()[0])
		s.setHeight(self.settings.value("H", -1).toInt()[0])
		self.settings.endGroup()
		if p.x() > 0 and p.y() > 0 and s.width() > 0 and s.height() > 0:
			self.resize(s)  # restore size
			self.move(p)  # restore position

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	deleteIcon16 = QIcon(":/images/delete-16.png")
	addIcon16 =  QIcon(":/images/add-16.png")
	renameIcon16 = QIcon(":/images/rename-16.png")

	if sys.platform == 'win32':
		app.setStyle("windowsxp")  # required for windows 8!
	else:
		if sys.platform == 'darwin':
			app.setStyle("macintosh")
		else:
			app.setStyle("plastique");
	mw = ImageDiff()
	app.mw = mw

	app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
	mw.show()
	mw.saveSettings()
	sys.exit(app.exec_())

