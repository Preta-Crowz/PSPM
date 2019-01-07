import sys, json
from os import path
from re import match
from time import asctime
from webbrowser import open as web
from locale import getdefaultlocale
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore

ui = uic.loadUiType("assets/pspm.ui")[0]

fileList = open("assets/order.json","r",encoding="utf-8")
fileList = json.load(fileList)

qtList = open("assets/order.json","r",encoding="utf-8")
qtList = json.load(qtList)
qtList = json.dumps(qtList)
for char in "abcdefghilmnpqrstw":
    qtList = qtList.replace("-"+char,char.upper())
qtList = json.loads(qtList.replace(".p","P"))

getObjAttr = {
    "QSlider": "value",
    "QSpinBox": "value",
    "QCheckBox": "isChecked",
    "QPlainTextEdit": "toPlainText",
    "QLineEdit": "text"
}

setObjAttr = {
    "QSlider": "setValue",
    "QSpinBox": "setValue",
    "QCheckBox": "setChecked",
    "QPlainTextEdit": "setPlainText",
    "QLineEdit": "setText"
}

wType = [
    "Default",
    "Flat",
    "Large Biomes",
    "Amplified",
    "Buffet"
]



class pspm(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.closeBtn.clicked.connect(self.btnClose)
        self.loadBtn.clicked.connect(self.btnLoad)
        self.saveBtn.clicked.connect(self.btnSave)
        self.resetBtn.clicked.connect(self.reset)
        self.gitBtn.clicked.connect(self.github)

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
        global qtList, fileList, objAttr
        fileName = QFileDialog.getSaveFileName(self,filter="*.properties")[0]
        if fileName == "": return
        if not fileName.endswith(".properties"):
            fileName += ".properties"
        data = open("assets/base.properties","r",encoding="utf-8").read()
        temp = [asctime()]
        temp = temp + (["{}"] * (data.count("{}")-1))
        temp = "\",\"".join(temp)
        data = eval("data.format(\"{}\")".format(temp))
        base = open("assets/base.json","r",encoding="utf-8")
        base = json.load(base)
        for i in range(41):
            obj = getattr(self,qtList[i])
            objType = match("\<class \'PyQt5\.QtWidgets\.(.*)\'\>",str(type(obj)))[1]
            if objType == "QComboBox":
                value = obj.currentText().upper()
            else:
                value = getattr(obj,getObjAttr[objType])()
            if value is True:
                value = "true"
            elif value is False:
                value = "false"
            if fileList[i] == "resource-pack" or fileList[i] == "level-name":
                value = value.replace(":","\\:")
                value = value.replace("=","\\=")
                value = value.replace("\'","\\\'")
            elif fileList[i] == "motd":
                if len(value) > 59:
                    value = value[:59]
                value = value.encode("raw_unicode_escape")
                value = eval(str(value)[1:])
            elif fileList[i] == "level-type" and value == "LARGE BIOMES":
                value = "LARGEBIOMES"
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
        properties = properties.split("\n")
        for prop in properties:
            matched = match("^(.+)\=(.*)$",prop)
            if not matched: continue
            propName = matched[1]
            value = matched[2]
            if not propName in fileList: continue
            i = fileList.index(matched[1])
            obj = getattr(self,qtList[i])
            objType = match("\<class \'PyQt5\.QtWidgets\.(.*)\'\>",str(type(obj)))[1]
            if fileList[i] == "level-type":
                value = value[0] + value[1:].lower()
                if value == "Largebiomes":
                    value = "Large Biomes"
                elif not value in wType:
                    value = "Default"
                index = wType.index(value)
                obj.setCurrentIndex(index)
            else:
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                elif match("\d*",value)[0] != "": value = int(value)
                getattr(obj,setObjAttr[objType])(value)

    def reset(self):
        self.load("assets/default.properties")

    def github(self):
        web("https://github.com/Preta-Crowz/PSPM")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    base_path = path.abspath(".")
    locale = getdefaultlocale()[0]
    try:
        lang_path = path.join(base_path, 'lang', 'Lang_{}.qm'.format(locale))
        translator = QtCore.QTranslator(app)
        translator.load(lang_path)
    except:
        lang_path = path.join(base_path, 'lang', 'Lang_en_US.qm')
        translator = QtCore.QTranslator(app)
        translator.load(lang_path)
    app.installTranslator(translator)
    win = pspm()
    win.show()
    app.exec_()