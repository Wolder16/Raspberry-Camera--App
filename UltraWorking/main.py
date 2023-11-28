from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QLCDNumber
import pyqtgraph as pg
import sys

# https://stackoverflow.com/questions/35932660/qcombobox-click-event обновление по клику

app = QtWidgets.QApplication([])
ui = uic.loadUi("designtest.ui")
ui.setWindowTitle("SerialGUI")

visota = 0

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)


posX = 200
posY = 100
listX = []
for x in range(100): listX.append(x)
listY = []
for x in range(100): listY.append(0)


def onRead():
    if not serial.canReadLine(): return     # выходим если нечего читать
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    if data[0] == '0':
        global listX
        global listY
        listY = listY[1:]
        listY.append(int(data[2]))



def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)


def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())


def onClose():
    serial.close()

def MNP1OP(val):
    serialSend([1, val])

def MNP1CLS(val):
    serialSend([2, val])

def MNP2OP(val):
    serialSend([3, val])

def MNP2CLS(val):
    serialSend([4, val])

def MNP3OP(val):
    serialSend([5, val])

def MNP3CLS(val):
    serialSend([6, val])

def StolUp(val):
    serialSend([7, val])


def StolDown(val):
    serialSend([8, val])



serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)


ui.manipB1_1.clicked.connect(MNP1CLS)
ui.manipB1_2.clicked.connect(MNP1OP)

ui.manipB2_1.clicked.connect(MNP2CLS)
ui.manipB2_2.clicked.connect(MNP2OP)

ui.manipB3_1.clicked.connect(MNP3CLS)
ui.manipB3_2.clicked.connect(MNP3OP)

ui.Stol_up.clicked.connect(StolUp)
ui.Stol_down.clicked.connect(StolDown)

ui.show()
app.exec()



