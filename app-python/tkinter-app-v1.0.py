import serial
from tkinter import *
from tkinter import messagebox as mb

arduino_serial = serial.Serial('COM3', baudrate = 9600, timeout = 1)

flag_mode = "m_to_l"
flag_button = False
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
            sym += 'err' #oшибка при чтении символа
            continue;
        if value == ' ':
            sym += ' '
            continue
        if sym == '':
            sym += result
        else:
            sym += ' ' + result
    return sym


def to_latter_sym(kod):
    flag = 0
    for key, value in latin_alphabet.items():
        if kod == value:
            flag = 1
            sym = key
    if flag == 0:
        return "SYMERR"
    return sym

def to_latter_stroka(kod_str):
    stroka = ''
    kod_str = kod_str.split(' ')
    for kod in kod_str:
        if kod == '':
            sym = ' '
        else:
            sym = to_latter_sym(kod)
            if sym == "SYMERR":
                stroka += ' err' #шибка при чтении символа
                continue;
        stroka += sym 
    return stroka
def clearall():
    tw_input['state'] = NORMAL
    tw_output['state'] = NORMAL
    tw_input.delete(0.0, END)
    tw_output.delete(0.0, END)
    tw_input['state'] = DISABLED
    tw_output['state'] = DISABLED
def clearin():
    tw_input['state'] = NORMAL
    tw_input.delete(0.0, END)
    tw_input['state'] = DISABLED
def clearout():
    tw_input['state'] = NORMAL
    tw_output.delete(0.0, END)
    tw_output['state'] = DISABLED
def team():
    info_txt = "Команды юных разработчкив, которые разработали алгоритм дешифровки кода Морзе!\n\
                Маснуров Владислав\n\
                Мырзабеков Рамис\n\
                Руденко Максим\n\
                Громов Дмитрий"
    mb.showinfo("AVOCADO TEAM", info_txt)
def info():
    info_txt = "Приложение со вместо принимает код Морзе и дешифрует его в символы латиницы.\n\
                Имеется в данныый момент только один режим - Азбука Морзе -> Латиница\n"
    mb.showinfo("AVOCADO TEAM", info_txt)
#------------------------------------------------->Function
'''
def change_to_morze():
    global flag_mode, button_text
    if (flag_mode == 'l_to_m'):
        flag_mode = 'm_to_l'
        #arduino_serial.write(flag_mode.encode())
        modes['text'] = "﹝Латиница ⟶ Азбука Морзе﹞"
        tw_input['state'] = NORMAL
        bw_convert['text'] = 'Передача'
def change_to_letter():
    global flag_mode, button_text
    if (flag_mode != 'l_to_m'):
        flag_mode = 'l_to_m'
        #arduino_serial.write(flag_mode.encode())
        modes['text'] = "﹝Азбука Морзе ⟶ Латиница﹞"
        tw_input['state'] = DISABLED
        bw_convert['text'] = 'Прием'
def function_arduino():
    global flag_button
    flag_button = True
'''  
#------------------------------------------------> COLORS AND SOME VARS
widget_color = 'LightBlue'
root_color = 'LightCyan'
button_text = 'Прием'
run = True
stroka = ''
# Создаем  окно приложения
window = Tk()
window['bg'] = root_color
window.title("Азбука Морзе - Avocado")
window.geometry('550x469')
window.resizable(width =  False, height = False)
        
# Настройка меню
main_menu = Menu(window)
mode_menu = Menu(main_menu, tearoff = 0)
option_menu = Menu(main_menu, tearoff = 0)
info_menu = Menu(main_menu, tearoff = 0)
window.config(menu=main_menu)

main_menu.add_cascade(label='Режимы', menu=mode_menu)
#mode_menu.add_command(label='Азбука Морзе ⟶ Латиница', command=change_to_letter)
#mode_menu.add_command(label='Латиница ⟶ Азбука Морзе', command=change_to_morze)
main_menu.add_cascade(label='Настройки', menu=option_menu)
option_menu.add_command(label='Очистить все поля', command=clearall)
option_menu.add_command(label='Очистить поле ввода', command=clearin)
option_menu.add_command(label='Очистить поле вывода', command=clearout)
main_menu.add_cascade(label='Справки', menu=info_menu)
info_menu.add_command(label='Команда', command=team)
info_menu.add_command(label='Приложение', command=info)
info_menu.add_command(label='Азбука Морзе')
#main_menu.add_command(label='Выход')


tw2_label = Label(window, text="Азбука Морзе", font="Arial 10 italic")
tw1_label = Label(window, text="Простой текст", font="Arial 10 italic")

tw_input = Text(window, height=10, width=60, bg=widget_color, font="Arial 10", state=DISABLED)
tw_output = Text(window, height=10, width=60, bg=widget_color, font="Arial 10 bold", state=DISABLED)
tw1_label.place(x=60,y=15)
tw_input.place(x=60,y=35)
tw2_label.place(x=60,y=205)
tw_output.place(x=60,y=225)
modes = Label(window, text="﹝Азбука Морзе ⟶ Латиница﹞", font="Arial 10 bold", bg='LightCyan')
bw_convert = Button(window, text='Прием',height=1, width=10, bg='Gainsboro', font="Arial 10")
bw_convert.place(x=220, y=400)
modes.place(x=330,y=0)

while run:
    try:
        
        #window.update_idletasks()
        window.update()
    except:
        break
    
    if flag_mode == 'm_to_l':
        analogData = arduino_serial.readline().decode()
        if analogData == '\r\n':
            arduino_serial.write(b'InErr')
            print("Ошибка")
            continue
          
        analogData = analogData.split('\r\n')
        if (analogData[0] == ''):
            continue
        tw_input['state'] = NORMAL
        tw_output['state'] = NORMAL
        tw_input.insert(END, analogData[0])
        tw_output.insert(END, to_morse_sym(analogData[0]) + ' ')
        tw_input['state'] = DISABLED
        tw_output['state'] = DISABLED
    #if flag_mode == 'l_to_m':
    #   stroka = tw_input.get(1.0, END)
    #    print(stroka)
    #    arduino_serial.write(stroka.encode())
    #    tw_output['state'] = NORMAL
    #    tw_output.insert(1.0, to_morse_stroka(stroka))
    #   tw_output['state'] = DISABLED
    #   flag_button = False
    
    
        
