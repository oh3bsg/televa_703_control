# https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi
import tkinter as tk
import tkinter.font as tkFont
import time
from smbus import SMBus

# MCP23017 registers
IODIRA = 0x00  # IO direction A - 1= input 0 = output
IOCON  = 0x0A  # Configuration register

global div
global frq_view
global i2cbus
global i2caddress
div=0

def update(div):
    """ Update PLL and display """
    global frq_view
    global i2cbus
    global i2caddress

    hz2=div*25+160325
    hz_text= str(hz2)
    
    # Send divider to PLL
    i2cbus.write_byte_data(i2caddress, GPIOA, div)

    # Update frequency display
    for index in range(0, 6):
        frq_view[index]["text"] = hz_text[index]

def bt_100_up():
    update_check(256)

def bt_100_down():
    update_check(-256)

def bt_10_up():
    update_check(256)

def bt_10_down():
    update_check(-256)

def bt_1_up():
    update_check(40)

def bt_1_down():
    update_check(-40)

def bt_0_1_up():
    update_check(4)

def bt_0_1_down():
    update_check(-4)

def bt_0_01_up():
    update_check(1)

def bt_0_01_down():
    update_check(-1)

def bt_0_001_up():
    update_check(256)

def bt_0_001_down():
    update_check(-256)

def update_check(value):
    global div

    new_div = div + value
    if new_div >= 0 and new_div <= 255:
        div = new_div
        update(div)

def create_frequency_view(root):
    view = []

    for index, offset in enumerate(frq_x_pos):
        label=tk.Label(root)
        ft = tkFont.Font(family='Times',size=25)
        label["bg"] = "#187631"
        label["font"] = ft
        label["borderwidth"] = "4px"
        label["fg"] =  "#f7d416"
        label["justify"] = "center"
        label["text"] = "0"
        label["relief"] = "sunken"
        label.place(x=offset,y=70,width=40,height=71)
        view.append(label)

        bt_up=tk.Button(root)
        bt_up["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        bt_up["font"] = ft
        bt_up["borderwidth"] = "4px"
        bt_up["fg"] = "#000000"
        bt_up["justify"] = "center"
        bt_up["text"] = ""
        bt_up["relief"] = "raised"
        bt_up.place(x=offset,y=30,width=40,height=30)
        bt_up["command"] = frq_up_cb[index]

        bt_down=tk.Button(root)
        bt_down["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        bt_down["font"] = ft
        bt_down["borderwidth"] = "4px"
        bt_down["fg"] = "#000000"
        bt_down["justify"] = "center"
        bt_down["text"] = ""
        bt_down.place(x=offset,y=150,width=40,height=30)
        bt_down["command"] = frq_down_cb[index]

    label=tk.Label(root)
    ft = tkFont.Font(family='Times',size=100)
    label["bg"] = "#000000"
    label["font"] = ft
    label["borderwidth"] = "1px"
    label["fg"] =  "#000000"
    label["justify"] = "center"
    label["text"] = "."
    label["relief"] = "flat"
    label.place(x=180,y=130,width=10,height=10)

    return view

frq_x_pos = [30, 80, 130, 200, 250, 300]
frq_up_cb = [bt_100_up, bt_10_up, bt_1_up, bt_0_1_up, bt_0_01_up, bt_0_001_up]
frq_down_cb = [bt_100_down, bt_10_down, bt_1_down, bt_0_1_down, bt_0_01_down, bt_0_001_down]


def main():
    global frq_view
    global i2cbus
    global i2caddress

    root = tk.Tk()
    root.title("TELEVA 703-LYVV Control")
    width=370
    height=210
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=True, height=True)

    frq_view = create_frequency_view(root)

    i2cbus = SMBus(1)  # Create a new I2C bus
    i2caddress = 0x20  # Address of MCP23017 device
    i2cbus.write_byte_data(i2caddress, IOCON, 0x02)  # Update configuration register
    i2cbus.write_word_data(i2caddress, IODIRA, 0xFF00)  # Set Port A as outputs and Port B as inputs

    update(div)
    root.mainloop()

if __name__ == "__main__":
    main()