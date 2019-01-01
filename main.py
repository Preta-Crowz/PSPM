import sys, json, time
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

ui = uic.loadUiType("main.ui")[0]

qtList = open("order.json","r",encoding="utf-8")
qtList = json.load(qtList)
qtList = json.dumps(qtList)
fileList = open("order.json","r",encoding="utf-8")
fileList = json.load(fileList)
for char in "abcdefghilmnpqrstw":
    qtList = qtList.replace("-"+char,char.upper())
qtList = json.loads(qtList.replace(".p","P"))

class pspm(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.closeBtn.clicked.connect(self.btnClose)
        self.loadBtn.clicked.connect(self.btnLoad)
        self.saveBtn.clicked.connect(self.btnSave)
        self.resetBtn.clicked.connect(self.reset)

    def btnClose(self):
        app.quit()
        sys.exit(0)

    def btnLoad(self):
        fileName = QFileDialog.getOpenFileName(self,filter="*.properties")[0]
        if fileName == "": return
        if not fileName.endswith(".properties"):
            fileName += ".properties"
        self.load(fileName)

    def btnSave(self):
        global qtList, fileList
        fileName = QFileDialog.getSaveFileName(self,filter="*.properties")[0]
        if fileName == "": return
        if not fileName.endswith(".properties"):
            fileName += ".properties"
        data = open("base.properties","r",encoding="utf-8").read()
        temp = [time.asctime()]
        temp = temp + (["{}"] * (data.count("{}")-1))
        temp = "\",\"".join(temp)
        data = eval("data.format(\"{}\")".format(temp))
        base = open("base.json","r",encoding="utf-8")
        base = json.load(base)
        for i in range(41):
            obj = getattr(self,qtList[i])
            if type(obj) == QSlider:
                value = obj.value()
            elif type(obj) == QSpinBox:
                value = obj.value()
            elif type(obj) == QCheckBox:
                value = obj.isChecked()
            elif type(obj) == QPlainTextEdit:
                value = obj.toPlainText()
            elif type(obj) == QLineEdit:
                value = obj.text()
            elif type(obj) == QComboBox:
                value = obj.currentText().upper()
            base[fileList[i]] = value
        for prop in fileList:
            temp = [str(base[prop])]
            temp = temp + (["{}"] * (data.count("{}")-1))
            temp = "\",\"".join(temp)
            data = eval("data.format(\"{}\")".format(temp))
        open(fileName,"w",encoding="utf-8").write(data)

    def load(self,fileName):
        global qtList, fileList
        file = open(fileName,"r",encoding="utf-8")
        properties = file.read()

    def reset(self):
        self.load("default.properties")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = pspm()
    win.show()
    app.exec_()