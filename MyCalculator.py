from enum import Enum
from tkinter.ttk import Label, Button, Combobox, Radiobutton

import serial
from serial.tools import list_ports
from tkinter import Tk, StringVar, ttk, messagebox
import tkinter as tk
import logging
import threading
import time
from utility import Utility
from tkinter import scrolledtext

connected = False
baudrate = 115200
comport_number = 'COM22'


class ENDTRAIL(Enum):
    WINDOWS_SLASH_RN = '\r\n'
    SLASH_R = '\r'
    SLASH_N = '\n'
    NOTHING = ''


def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


serial_port = serial.Serial()

root = tk.Tk()
root.title("Serial Play")

frame_choose_port = tk.Frame(root,background="blue")
frame_choose_options = tk.Frame(root,background="red")
frame_view_log = tk.Frame(root,background="green")
frame_sendto_port = tk.Frame(root,background="yellow")

value = StringVar()

utility = Utility()

cb_ports = Combobox(frame_choose_port, textvariable=value, state='readonly',
                                 width=utility.calculate_combo_width(list_ports.comports()))
# ports = serial.tools.list_ports.comports()

# print([port.device for port in ports])
cb_ports['values'] = list_ports.comports()
cb_ports.current(0)

cb_bauderates = Combobox(frame_choose_options,state='readonly',width=10)
lb_bauderates = Label(frame_choose_options, text="Baud")
cb_bauderates['values'] = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
cb_bauderates.current(6)  # 9600 default option

MODES = [
    ("Monochrome", "1"),
    ("Grayscale", "L"),
    ("True color", "RGB"),
    ("Color separation", "CMYK"),
]

v = StringVar()
v.set("L")  # initialize

group = tk.LabelFrame(frame_choose_options, text="Group", padx=5, pady=5)

rd_parity_none = Radiobutton(group, text="none", variable=v, value=1).grid(column=0, row=0, sticky='W')
rd_parity_odd = Radiobutton(group, text="odd", variable=v, value=2).grid(column=0, row=1, sticky='W')
rd_parity_even = Radiobutton(group, text="even", variable=v, value=3).grid(column=0, row=2, sticky='W')
rd_parity_mark = Radiobutton(group, text="mark", variable=v, value=4).grid(column=0, row=3, sticky='W')
rd_parity_space = Radiobutton(group, text="space", variable=v, value=5).grid(column=0, row=4, sticky='W')


txt_logs = scrolledtext.ScrolledText(frame_view_log,width= 48, height= 30)

def handle_data(data):
    pass


def read_from_port(ser):
    while ser.inWaiting and connected:
        try:
            txt_logs.insert(tk.END, ser.readline())
            txt_logs.see("end")
        except RuntimeError:
            print("Error")
            pass


def connect_to_port(port_number, baud):
    global serial_port
    serial_port = serial.Serial(port_number, baud)


def click_me():
    global connected
    if not connected:
        clear_terminal()
        btn_start_stop['text'] = 'Stop'
        connected = True
        connect_to_port(list_ports.comports()[cb_ports.current()].device, cb_bauderates.get())
        thread = threading.Thread(target=read_from_port, args=(serial_port,))
        thread.start()
    else:
        connected = False
        serial_port.close()
        btn_start_stop['text'] = 'Start'


btn_start_stop = Button(frame_choose_port, text="Start", command=click_me)

def clear_terminal():
    txt_logs.delete('1.0', tk.END)


action_clear = Button(frame_view_log, width=3, text="C", command=clear_terminal)

write_string = tk.StringVar(frame_sendto_port)


def write_to_port(ENDTRAIL=ENDTRAIL.SLASH_R):

    outstr = st = write_string.get()

    if len(outstr) ==0:
        return

    # removing last character
    outstr = outstr[:-1]

    if (ENDTRAIL == ENDTRAIL.SLASH_R):
        outstr = outstr + ENDTRAIL.SLASH_R
    elif (ENDTRAIL == ENDTRAIL.SLASH_N):
        outstr = outstr + ENDTRAIL.SLASH_N
    elif (ENDTRAIL == ENDTRAIL.WINDOWS_SLASH_RN):
        outstr = outstr + ENDTRAIL.WINDOWS_SLASH_RN
    else:
        # ENDTRAIL.NOTHING
        pass

    serial_port.write(outstr)
    txt_send_command.delete('0', tk.END)


def btn_send_str_event():
    if connected:
        write_to_port()


def txt_send_str_event(event):
    if event.char == '\r' and connected:
        write_to_port()


txt_send_command = tk.Entry(frame_sendto_port, textvariable=write_string,width= 55)
txt_send_command.bind('<Key>', txt_send_str_event)

btn_send_command = Button(frame_sendto_port, text="Start", command=btn_send_str_event)

# lbl3 = Label(root, text="Review", width=10)
# lbl3.grid(column=1, row=2)


def on_close():
    global connected
    print("Bye!")
    close = messagebox.askokcancel("Close", "Would you like to close the program?")
    if close:
        connected = False
        root.destroy()

#buttonA0.grid(column = 0, row = 0, rowspan = 5, sticky = NE+SW)
#buttonB0.grid(column = 0, row = 5, columnspan = 2, sticky = E+W)
cb_ports.grid(column=0, row=0,sticky='W')
btn_start_stop.grid(column=1, row=0)
frame_choose_port.grid(column=0, row=0, sticky='W')

lb_bauderates.grid(column=0, row=0,sticky='N')
cb_bauderates.grid(column=1, row=0,sticky='N')
group.grid(column=0, row=1,columnspan=2)
frame_choose_options.grid(column=1, row=1,sticky='NS')

txt_logs.grid(column=0, row=0)
action_clear.grid(column=1, row=0, sticky="SE")
frame_view_log.grid(column=0, row=1)

txt_send_command.grid(column=0, row=0, sticky="EW")
btn_send_command.grid(column=1, row=0, sticky="E")
frame_sendto_port.grid(column=0, row=3,sticky='W')


root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
