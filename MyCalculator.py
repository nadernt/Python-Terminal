from enum import Enum
from tkinter.ttk import Label, Button, Combobox, Radiobutton, Spinbox

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


class ENDTRAIL():
    WINDOWS_SLASH_RN = "\r\n"
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

bg = ["blue","red","black","green","yellow"]

# comment below lines to add background color to frames.
for index in range(len(bg)):
    bg[index] = None

frame_choose_port = tk.Frame(root, background=bg[0])
frame_choose_options = tk.Frame(root, background=bg[1])
#frame_trail = tk.Frame(root, background=bg[2])
frame_view_log = tk.Frame(root, background=bg[3])
frame_sendto_port = tk.Frame(root, background=bg[4])

value = StringVar()

utility = Utility()

cb_ports = Combobox(frame_choose_port, textvariable=value, state='readonly',
                    width=utility.calculate_combo_width(list_ports.comports()))
# ports = serial.tools.list_ports.comports()

# print([port.device for port in ports])
cb_ports['values'] = list_ports.comports()
cb_ports.current(0)

cb_bauderates = Combobox(frame_choose_port, state='readonly', width=10)
lb_bauderates = Label(frame_choose_port, text="Baud")
cb_bauderates['values'] = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
cb_bauderates.current(11)  # 9600 default option

val_parity = StringVar()
val_parity.set('N')  # initialize

lbframe_parity = tk.LabelFrame(frame_choose_options, text="Parity", padx=5, pady=5)
# PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'

rd_parity_none = Radiobutton(lbframe_parity, text="none", variable=val_parity, value='N').grid(column=0, row=0,
                                                                                               sticky='W')
rd_parity_odd = Radiobutton(lbframe_parity, text="odd", variable=val_parity, value='O').grid(column=0, row=1,
                                                                                             sticky='W')
rd_parity_even = Radiobutton(lbframe_parity, text="even", variable=val_parity, value='E').grid(column=0, row=2,
                                                                                               sticky='W')
rd_parity_mark = Radiobutton(lbframe_parity, text="mark", variable=val_parity, value='M').grid(column=0, row=3,
                                                                                               sticky='W')
rd_parity_space = Radiobutton(lbframe_parity, text="space", variable=val_parity, value='S').grid(column=0, row=4,
                                                                                                 sticky='W')
# val_parity.set(1)

val_databits = tk.IntVar()
val_databits.set(serial.EIGHTBITS)  # initialize

lbframe_databits = tk.LabelFrame(frame_choose_options, text="Parity", padx=5, pady=5)
rd_8bit = Radiobutton(lbframe_databits, text="8 bits", variable=val_databits, value=serial.EIGHTBITS).grid(column=0,
                                                                                                           row=0,
                                                                                                           sticky='W')
rd_7bit = Radiobutton(lbframe_databits, text="7 bits", variable=val_databits, value=serial.SEVENBITS).grid(column=0,
                                                                                                           row=1,
                                                                                                           sticky='W')
rd_6bit = Radiobutton(lbframe_databits, text="6 bits", variable=val_databits, value=serial.SIXBITS).grid(column=0,
                                                                                                         row=2,
                                                                                                         sticky='W')
rd_5bit = Radiobutton(lbframe_databits, text="5 bits", variable=val_databits, value=serial.FIVEBITS).grid(column=0,
                                                                                                          row=3,
                                                                                                          sticky='W')
# val_databits.set(8)


val_stopbits = tk.IntVar()
val_stopbits.set(1)  # initialize

lbframe_stopbits = tk.LabelFrame(frame_choose_options, text="Stop Bits", padx=5, pady=5)

rd_1bit = Radiobutton(lbframe_stopbits, text="1 bit", variable=val_stopbits, value=1).grid(column=0, row=0, sticky='W')
rd_2bits = Radiobutton(lbframe_stopbits, text="2 bits", variable=val_stopbits, value=2).grid(column=0, row=1,
                                                                                             sticky='W')
# val_stopbits.set(1)

val_hwflowcontrol = StringVar()
val_hwflowcontrol.set(0)  # initialize

lbframe_hwflowcontrol = tk.LabelFrame(frame_choose_options, text="Hardware Flow Control", padx=5, pady=5)

rd_hw_none = Radiobutton(lbframe_hwflowcontrol, text="None", variable=val_hwflowcontrol, value=0).grid(column=0, row=0,
                                                                                                       sticky='W')
rd_hw_dtr_dsr = Radiobutton(lbframe_hwflowcontrol, text="DTR/DSR", variable=val_hwflowcontrol, value=1).grid(column=0,
                                                                                                             row=1,
                                                                                                             sticky='W')
rd_hw_rts_cts = Radiobutton(lbframe_hwflowcontrol, text="RTS/CTS", variable=val_hwflowcontrol, value=2).grid(column=0,
                                                                                                             row=2,
                                                                                                             sticky='W')
rd_hw_rs485_rts = Radiobutton(lbframe_hwflowcontrol, text="RS485-RTS", variable=val_hwflowcontrol, value=3).grid(
    column=0, row=3, sticky='W')
# val_hwflowcontrol.set(2)


val_xonxoff = tk.IntVar()
val_xonxoff.set(0)  # initialize

lbframe_xonxoff = tk.LabelFrame(frame_choose_options, text="Software Flow Control", padx=5, pady=5)

rd_xon = Radiobutton(lbframe_xonxoff, text="Xon", variable=val_xonxoff, value=0).grid(column=0, row=0, sticky='W')
rd_xoff = Radiobutton(lbframe_xonxoff, text="Xoff", variable=val_xonxoff, value=1).grid(column=1, row=0, sticky='W')


val_trail = StringVar()
val_trail.set(ENDTRAIL.SLASH_N)  # initialize

lbframe_trail = tk.LabelFrame(frame_choose_options, text="Trail", padx=5, pady=5)

rd_r = Radiobutton(lbframe_trail, text="\\n", variable=val_trail, value=ENDTRAIL.SLASH_N).grid(column=0, row=0, sticky='W')
rd_n = Radiobutton(lbframe_trail, text="\\r", variable=val_trail, value=ENDTRAIL.SLASH_R).grid(column=1, row=0, sticky='W')
rd_nr = Radiobutton(lbframe_trail, text="\\r\\n", variable=val_trail, value=ENDTRAIL.WINDOWS_SLASH_RN).grid(column=0, row=1, sticky='W')
rd_notrail = Radiobutton(lbframe_trail, text="non", variable=val_trail, value=ENDTRAIL.NOTHING).grid(column=1, row=1, sticky='W')



val_timeout = StringVar(frame_sendto_port)

timeout = ["Wait Forever", "Non-blocking"]
for x in range(1, 61):
    timeout.append(str(x) + " Sec")

sp_timeout = Spinbox(frame_sendto_port, state='readonly', values=timeout, textvariable=val_timeout)
val_timeout.set("Wait Forever")

txt_logs = scrolledtext.ScrolledText(frame_view_log, width=48,height=35)


def handle_data(data):
    pass


def read_from_port(ser):
    while ser.inWaiting and connected:
        try:
            txt_logs.insert(tk.END, ser.readline())
            txt_logs.see("end")
        except Exception as ex:
            close_port()
            messagebox.showerror("Error", "Error: " + str(ex))


def connect_to_port(port_number, baud):
    global serial_port
    """
    Parameters:
    port – Device name or None.
    baudrate (int) – Baud rate such as 9600 or 115200 etc.
    bytesize – Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
    parity – Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
    stopbits – Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
    timeout (float) – Set a read timeout value.
    xonxoff (bool) – Enable software flow control.
    rtscts (bool) – Enable hardware (RTS/CTS) flow control.
    dsrdtr (bool) – Enable hardware (DSR/DTR) flow control.
    write_timeout (float) – Set a write timeout value.
    inter_byte_timeout (float) – Inter-character timeout, None to disable (default).
    exclusive (bool) – Set exclusive access mode (POSIX only). A port cannot be opened in exclusive access mode if it is already open in exclusive access mode.
        """
    try:
        vtimeout = val_timeout.get()

        if val_timeout.get() == "Wait Forever":
            vtimeout = None
        elif val_timeout.get() == "Non-blocking":
            vtimeout = float(0)
        else:
            vtimeout = float(val_timeout.get().replace(' Sec', ''))

        vrtscts = 0
        vdsrdtr = 0

        if val_hwflowcontrol.get() == 1:
            vrtscts = 1
        elif val_hwflowcontrol.get() == 3:
            vdsrdtr = 1
        print(val_databits.get())
        serial_port = serial.Serial(port=port_number, baudrate=baud, bytesize=val_databits.get(),
                                    parity=val_parity.get(), stopbits=val_stopbits.get(),
                                    timeout=vtimeout, xonxoff=val_xonxoff.get(), rtscts=vrtscts, dsrdtr=vdsrdtr)
    except ValueError:
        # handle ValueError exception
        pass
    except (OSError, serial.SerialException) as ex:
        close_port()
        messagebox.showerror("Error", "Error: " + str(ex))
    except Exception as ex:
        messagebox.showerror("Error", "Error: " + str(ex))
        close_port()


def close_port():
    global connected
    connected = False
    serial_port.close()
    btn_start_stop['text'] = 'Start'


def click_me():
    global connected
    if not connected:
        clear_terminal()
        btn_start_stop['text'] = 'Stop'
        connected = True
        connect_to_port(list_ports.comports()[cb_ports.current()].device, cb_bauderates.get())
        thread = threading.Thread(target=read_from_port, daemon=True, args=(serial_port,))
        thread.start()
    else:
        close_port()


btn_start_stop = Button(frame_choose_port, text="Start", command=click_me)


def clear_terminal():
    txt_logs.delete('1.0', tk.END)


action_clear = Button(frame_choose_options, width=3, text="C", command=clear_terminal)

write_string = tk.StringVar(frame_sendto_port)


def write_to_port(endtrail=ENDTRAIL.SLASH_R):
    try:
        outstr = write_string.get()

        if len(outstr) == 0:
            return

        # removing last character
        # outstr = outstr[:-1]

        if (endtrail == ENDTRAIL.SLASH_R):
            outstr = outstr + ENDTRAIL.SLASH_R
        elif (endtrail == ENDTRAIL.SLASH_N):
            outstr = outstr + ENDTRAIL.SLASH_N
        elif (endtrail == ENDTRAIL.WINDOWS_SLASH_RN):
            outstr = outstr + ENDTRAIL.WINDOWS_SLASH_RN
        else:
            # ENDTRAIL.NOTHING
            pass

        print(repr(outstr))
        serial_port.write(outstr.encode())
        txt_send_command.delete('0', tk.END)
    except Exception as ex:
        close_port()
        messagebox.showerror("Error", "Error: " + str(ex))


def btn_send_str_event():
    if connected:
        write_to_port(val_trail.get())


def txt_send_str_event(event):
    if event.char == '\r' and connected:
        write_to_port(val_trail.get())


txt_send_command = tk.Entry(frame_sendto_port, textvariable=write_string, width=55)
txt_send_command.bind('<Key>', txt_send_str_event)

btn_send_command = Button(frame_sendto_port, text="Start", command=btn_send_str_event)


def on_close():
    global connected
    print("Bye!")
    close = messagebox.askokcancel("Close", "Would you like to close the program?")
    if close:
        connected = False
        root.destroy()


# buttonA0.grid(column = 0, row = 0, rowspan = 5, sticky = NE+SW)
# buttonB0.grid(column = 0, row = 5, columnspan = 2, sticky = E+W)
cb_ports.grid(column=0, row=0, sticky='W')
btn_start_stop.grid(column=1, row=0)
lb_bauderates.grid(column=2, row=0)
cb_bauderates.grid(column=3, row=0)
frame_choose_port.grid(column=0, row=0, columnspan=4, sticky='W')


txt_logs.grid(column=0, row=0)
frame_view_log.grid(column=0, row=1,sticky='NSEW')

lbframe_parity.grid(column=0, row=0, sticky='WE')
lbframe_databits.grid(column=0, row=1, sticky='WE')
lbframe_stopbits.grid(column=0, row=2, sticky='WE')
lbframe_hwflowcontrol.grid(column=0, row=3, sticky='WE')
lbframe_xonxoff.grid(column=0, row=4, sticky='WE')
lbframe_trail.grid(column=0, row=5, sticky='WE')
action_clear.grid(column=0, row=6, sticky='WS')


frame_choose_options.grid(column=1, row=1, sticky='NEWS')

txt_send_command.grid(column=0, row=0, sticky='EW')
btn_send_command.grid(column=1, row=0, sticky='E')
sp_timeout.grid(column=2, row=0, sticky='E')
frame_sendto_port.grid(column=0, row=3, columnspan=2, sticky='W')

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
