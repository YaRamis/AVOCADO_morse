from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from tkinter import *
from tkinter import messagebox as mb


latin_alphabet = {'A': '.-',
                  'B': '-...',
                  'C': '-.-.',
                  'D': '-..',
                  'E': '.',
                  'F': '..-.',
                  'G': '--.',
                  'H': '....',
                  'I': '..',
                  'J': '.---',
                  'K': '-.-',
                  'L': '.-..',
                  'M': '--',
                  'N': '-.',
                  'O': '---',
                  'P': '.--.',
                  'Q': '--.-',
                  'R': '.-.',
                  'S': '...',
                  'T': '-',
                  'U': '..-',
                  'V': '...-',
                  'W': '-..-',
                  'X': '-..-',
                  'Y': '-.--',
                  'Z': '--..',
                  '0': '-----',
                  '1': '.----',
                  '2': '..---',
                  '3': '...--',
                  '4': '....-',
                  '5': '.....',
                  '6': '-....',
                  '7': '--...',
                  '8': '---..',
                  '9': '----.',
                  '.': '......',
                  ',': '.-.-.-',
                  ':': '---...',
                  ';': '-.-.-.',
                  '-': '-....-',
                  '!': '--..--',
                  '?': '..--..',
                  ' ': ' '
                  }


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

    def comand_info():
        tk = Tk()
        info_txt = "Команды юных разработчкив, которые разработали алгоритм дешифровки кода Морзе!\n\
                        Маснуров Владислав\n\
                        Мырзабеков Рамис\n\
                        Руденко Максим\n\
                        Громов Дмитрий"
        mb.showinfo("AVOCADO TEAM", info_txt)
        tk.mainloop()


    def app_des():
        tk = Tk()
        info_txt = "Приложение со вместо принимает код Морзе и дешифрует его в символы латиницы.\n\
                        Имеется в данныый момент только один режим - Азбука Морзе -> Латиница\n"
        mb.showinfo("AVOCADO TEAM", info_txt)
        tk.mainloop()



    def clean_first_field():
        ui.text_in_out.clear()

    def clean_second_field():
        ui.morse_out.clear()


    def clean_fields():
        ui.text_in_out.clear()
        ui.morse_out.clear()


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


    def to_morse_sym(sym):
        sym = sym.upper()
        sym = latin_alphabet.get(sym)
        if sym == None:
            return "SYMERR"
        return sym


    def to_morse_stroka(stroka):
        sym = ''
        i = -1
        for value in stroka:
            result = to_morse_sym(value)
            if result == "SYMERR":
                sym += 'err'  # oшибка при чтении символа
                continue;
            if value == ' ':
                sym += ' '
                continue
            if sym == '':
                sym += result
            else:
                sym += ' ' + result
        return sym


    def data_write():
        global in_str
        in_str = ui.text_in_out.toPlainText()
        in_str = str(in_str).upper()
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
        in_str = to_morse_stroka(in_str)
        ui.morse_out.setPlainText(in_str)


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
    ui.cleanB.clicked.connect(clean_fields)
    ui.clean_first.triggered.connect(clean_first_field)
    ui.clean_second.triggered.connect(clean_second_field)
    ui.clean_all.triggered.connect(clean_fields)
    ui.our_comand.triggered.connect(comand_info)
    ui.app_descrip.triggered.connect(app_des)
    ui.change_mode.currentIndexChanged.connect(change_mode)

ui.show()
app.exec()
