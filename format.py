# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import STYLE_MAP
# import pyperclip


def transfer(code, lineno=False, style='friendly',ulexer='C',):
	# 准备好格式
	lexer = get_lexer_by_name(ulexer)
	print(lexer)
	css = HtmlFormatter(style=style).get_style_defs()
	css = css + "\n.highlighttable { border: 1px solid #ddd; background-color: #f0f0f0; padding-left: 10px; " \
				"width:600px} "
	css = css + "\n."+ style + "table { border: 1px solid #ddd; background-color: #f0f0f0; padding-left: 10px; " \
				"width:600px} "
	if lineno:
		css = css + "\n.linenodiv { padding-right: 10px}"
	# print(css)
	with open("style.css", 'w', encoding='utf-8') as s:
		s.write(css)
	formatter = HtmlFormatter(linenos=lineno, style=style, cssclass=style)
	tmp_result = highlight(code, lexer, formatter)
	css_html = '<style type="text/css">' + css + '</style>'
	if not lineno:
		tmp_result = "<table class='highlighttable'><tbody><tr><td>" + tmp_result + "<td></tr></tbody" \
																					"></table> "
	result = "<html>" + css_html + tmp_result + "</html>"
	return result


class Ui_MainWindow(object):
	def __init__(self):
		self._style = None
		self._lineno = False
		self._lexer = 'C'

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(640, 512)
		MainWindow.setWindowIcon(QtGui.QIcon("biao.ico"))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		# browser config
		self.browser = QWebEngineView(self.centralwidget)
		self.browser.setGeometry(QtCore.QRect(325, 42, 300, 450))

		# Yes button config
		self.Yes_button = QtWidgets.QPushButton(self.centralwidget)
		self.Yes_button.setGeometry(QtCore.QRect(15, 10, 75, 23))
		self.Yes_button.setObjectName("Transfer！")
		self.Yes_button.clicked.connect(self.transfer_event)

		# style_combobox config
		self.style_combobox = QtWidgets.QComboBox(self.centralwidget)
		self.style_combobox.setGeometry(QtCore.QRect(100, 10, 150, 23))
		self.style_combobox.setObjectName("style")
		#self.style_combobox.addItem("Choose a style")
		for k in STYLE_MAP.keys():
			self.style_combobox.addItem(k)
		self.style_combobox.activated.connect(self.stylechange_event)

		# lexer_combobox config
		self.lexer_combobox = QtWidgets.QComboBox(self.centralwidget)
		self.lexer_combobox.setGeometry(QtCore.QRect(260, 10, 100, 23))
		self.lexer_combobox.setObjectName("lexer")
		self.lexer_combobox.addItem("C")
		self.lexer_combobox.addItem("Python")
		self.lexer_combobox.activated.connect(self.lexerchange_event)

		# check_box config
		self.lineno_checkbox = QtWidgets.QCheckBox("Line No.", self.centralwidget)
		self.lineno_checkbox.setGeometry(QtCore.QRect(400, 10, 80, 23))
		self.lineno_checkbox.setObjectName("check_box")
		self.lineno_checkbox.stateChanged.connect(self.lineno_event)

		# input_text config
		self.input_text = QtWidgets.QTextEdit(self.centralwidget)
		self.input_text.setGeometry(QtCore.QRect(15, 42, 300, 450))
		self.input_text.setObjectName("input_text")
		self.input_text.textChanged.connect(self.textchanged_event)

		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)

		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.Yes_button.setText(_translate("MainWindow", "Transfer"))

	# self.No_button.setText(_translate("MainWindow", "No"))

	def transfer_event(self):
		print("transfer")
		self.content = self.input_text.toPlainText()
		if self._style in STYLE_MAP.keys():
			code = transfer(self.content, self._lineno, self._style, self._lexer)
			self.browser.setHtml(code)

	def textchanged_event(self):
		print("text changed!")
		self.content = self.input_text.toPlainText()
		if self._style in STYLE_MAP.keys():
			code = transfer(self.content, self._lineno, self._style, self._lexer)
			self.browser.setHtml(code)

	def stylechange_event(self):
		print("style changed!")
		self._style = self.style_combobox.currentText()
		self.content = self.input_text.toPlainText()
		if self._style in STYLE_MAP.keys():
			code = transfer(self.content, self._lineno, self._style, self._lexer)
			self.browser.setHtml(code)

	def lineno_event(self):
		if self.lineno_checkbox.isChecked():
			self._lineno = True
		else:
			self._lineno = False
		self.content = self.input_text.toPlainText()
		if self._style in STYLE_MAP.keys():
			code = transfer(self.content, self._lineno, self._style, self._lexer)
			self.browser.setHtml(code)
		with open("test.html", 'w', encoding='utf-8') as f:
			f.write(code)

	def lexerchange_event(self):
		self._lexer = self.lexer_combobox.currentText()
		self.content = self.input_text.toPlainText()
		if self._style in STYLE_MAP.keys():
			code = transfer(self.content, self._lineno, self._style, self._lexer)
			self.browser.setHtml(code)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = QtWidgets.QMainWindow()
	window = Ui_MainWindow()
	window.setupUi(mainWindow)
	mainWindow.show()
	sys.exit(app.exec_())  # 运行程序
