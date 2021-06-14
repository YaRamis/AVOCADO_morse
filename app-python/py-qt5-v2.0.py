from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice

arduino_port = ''
mode_flag = "m_to_l"
in_str = ''

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")

serial = QSerialPort()
serial.setBaudRate(9600)

ports = QSerialPortInfo().availablePorts()
for port in ports:
    if port.portName() == 'COM3':
        arduino_port = port.portName()
        break

if arduino_port == '':
    ui.text_in_out.setPlainText("Не подключен Arduino!\nПожалуйста подключите и перезапустите приложение.")
    ui.text_in_out.zoomIn(5)
else:
    serial.setPortName(arduino_port)
    serial.open(QIODevice.ReadWrite)


    def data_read():
        global in_str
        if mode_flag == 'm_to_l':
            analogData = str(serial.readLine(), 'utf-8')
            if analogData == '\r\n':
                serial.write(b'InErr')
            elif analogData != '':
                in_str += analogData
                in_str = ''.join(in_str.split('\r\n'))
            ui.text_in_out.setPlainText(in_str)


    def data_write():
        global in_str
        in_str = ui.text_in_out.toPlainText()
        in_str = str(in_str).upper()
        print(in_str)
        if ' ' in in_str:
            in_str.split(' ')
            word = ''
            for i in range(len(in_str)):
                if in_str[i] == ' ' or in_str[i] == '\n':
                    serial.write(word.encode())
                    word = ''
                    continue
                word += in_str[i]
                if i == len(in_str) - 1:
                    serial.write(word.encode())
                    word = ''
        else:
            serial.write(str(in_str).encode())


    def change_mode():
        global mode_flag
        global in_str
        in_str = ''
        if mode_flag == "m_to_l":
            ui.text_in_out.setDisabled(False)
            ui.modeB.setDisabled(False)
            ui.text_in_out.clear()
            ui.morse_out.clear()
            ui.modeB.setText("Передача")
            mode_flag = "l_to_m"
            serial.write(b'l_to_m')
        elif mode_flag == "l_to_m":
            ui.text_in_out.setDisabled(True)
            ui.modeB.setDisabled(True)
            ui.text_in_out.clear()
            ui.morse_out.clear()
            ui.modeB.setText("Прием")
            mode_flag = "m_to_l"
            serial.write(b'm_to_l')

    serial.readyRead.connect(data_read)
    ui.modeB.clicked.connect(data_write)
    ui.change_mode.currentIndexChanged.connect(change_mode)

ui.show()
app.exec()
