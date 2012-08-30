#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from PyQt4 import QtGui,QtCore,uic
import simplejson

class MainWin(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.ui = uic.loadUi('ui/qjson.ui')
		self.ui.show()
		self.check(self.ui.tabWidget.currentIndex())
		self.connect(self.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.check)
		self.connect(self.ui.btnAdd, QtCore.SIGNAL('clicked()'), self.add_row)
		self.connect(self.ui.btnRemove, QtCore.SIGNAL('clicked()'), self.remove_row)
		self.connect(self.ui.btnWrite, QtCore.SIGNAL('clicked()'), self.write)

	def check(self, int_):
		if 'Link' in self.ui.tabWidget.tabText(int_):
			self.table = self.ui.tableLink
		elif 'Control' in self.ui.tabWidget.tabText(int_):
			self.table = self.ui.tableControl
		elif 'Error' in self.ui.tabWidget.tabText(int_):
			self.table = self.ui.tableError
		elif 'Result' in self.ui.tabWidget.tabText(int_):
			self.table = self.ui.tableResult
	
	def write(self):
		outfile = QtGui.QFileDialog.getSaveFileName()
		print outfile
		fh = codecs.open(outfile, mode='a+', encoding='utf-8')
		for rindex in range(self.table.rowCount()):
			for cindex in range(self.table.columnCount()):
				try:
					print self.table.item(rindex, cindex).text()
				except AttributeError:
					item = QtGui.QTableWidgetItem()
					item.setText('')
					self.table.setItem(rindex, cindex, item)
		fh.close()

	def add_row(self):
		self.table.insertRow(self.table.rowCount())
	
	def remove_row(self):
		self.table.removeRow(self.table.currentRow())


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mw = MainWin()
	sys.exit(app.exec_())

