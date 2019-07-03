#!/usr/bin/env python3
# -*- coding: utf8 -*-


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import serial  # module is pyserial


class Communication:

    def find_serial_port():
        """
        This function finds first available
        serial port for use and saves it into
        file port.text
        """

        with open('port.txt', 'w') as f:  # Open File port.txt
            for port_num in range(1, 255):  # Generate Port Numbers

                try:
                    # Test for serial port
                    serial.Serial(("COM" + str(port_num)))
                    # Write port number to file
                    f.write(("COM" + str(port_num)))
                    # return found port
                    return "COM" + str(port_num)

                except:
                    continue

        return -1

    def read_from_rs232(self, serial_port: str, address: str):
        """
        Module reads data from rs232 port, address starts with ME,
        and a hex value is added. eg ME034 ~ ME0ff, it is then sent
        in an ASCII encode

        @parameter address: type string
        @rtype: ASCII string
        """
        if serial_port.is_open:
            # Set delay for slow drive response
            time.sleep(.2)
            # Write address to serial port
            serial_port.write(address + '\r').encode()
            # Delay for slow drive response
            time.sleep(.2)
            # Return the data read from serial port
            return serial_port.readline()[-5:-1].decode('ascii')

        else:
            return -1

    def write_to_rs232(self, serial_port, address: str, parameter: str):
        """
        Module writes data from rs232 port, address starts with ME,
        and a hex value is added. eg ME034 ~ ME0ff, it is then sent
        in an ASCII encode, parameters range from 0000 ~ ffff and
        are also sent in ASCII encode.

        @param address: type string
        @param parameter: type string

        @rtype: None
        """
        if serial_port.is_open:

            if address != 'Save':
                # Send address to drive ready to recieve parameter(ME034~ME0ff)
                serial_port.write((address + '\r').encode('ascii'))
                # Set delay for slow drive response
                time.sleep(1)
                # Send parameter to drive address used in serial_port.write
                # above (0000~ffff)
                serial_port.write((parameter + '\r').encode('ascii'))
                return
            else:
                # Send ASCII 'S' including carridge return to get drive1
                # to save data permanently
                serial_port.write(('S\r')).encode('ascii')
                # Set delay for save time
                time.sleep(5)
                return
        else:
            return -1


class Application(Frame):

    def __init__(self, master):

        choice = ['', '', '']  # default selection

        Frame.__init__(self, master)
        self.pack(fill=BOTH, expand=1)
        # root.attributes('-fullscreen', True)  # Auto Full screen
        root.config(borderwidth=8, width=1, bg='Black')
        self.config(bg='grey5')

        root.minsize(800, 480)
        root.maxsize(800, 480)

        for row in range(0, 12):
            self.grid_rowconfigure(row, weight=1)

        for col in range(0, 7):
            if col <= 5:
                self.grid_columnconfigure(col, weight=1)
            else:
                self.grid_columnconfigure(col, weight=0)

        def ask_question():
            """
            Module pops up a small window checking that user does want to quit
            """
            if messagebox.askyesno('Question', 'Do you want to Quit?') == True:
                sys.exit()

        def help():

            popup = Toplevel()
            popup.title("HELP?")
            # Comment out the following line when using minsize, maxsize
            # popup.attributes('-fullscreen', True)  # Auto Full screen
            popup.minsize(800, 480)  # uncomment if want to restrict size
            popup.maxsize(800, 480)  # uncomment if want to restrict size
            popup.grid_rowconfigure(2, weight=1)
            popup.grid_columnconfigure(1, weight=1)

            message = "Make selection from Top 3 choices (WINDER,UNWINDER,BUFFER).\n"\
                "Next follow allowable button option, they will highlight with white text\n"\
                "and you will also see an arrow on the right side, as you move along through\n"\
                "the selection process, you will see the very right purple label change and\n"\
                "will show what you have selected. ensure you check this before selecting the \n"\
                "read or writes buttons\n"\
                "\n"\
                "Read Button - read data from Socapel drive and save to file\n"\
                "Write Button - read data from file and save to socapel drive"

            canvas = Canvas(popup)
            canvas.pack(fill="both", expand=True)

            frame = Frame(canvas)
            label = Label(canvas, text=message, bg="gray",
                          fg="black", font=('Times', '16', 'bold'),
                          borderwidth=3, relief=RIDGE, justify=CENTER)
            label.pack(fill="both", expand=True)

            vas1 = Button(canvas, text='CLOSE', bg='green',
                          font=('Times', '16', 'bold'), padx=0, pady=0,
                          borderwidth=3, relief=RIDGE, activebackground='MediumPurple3',
                          command=popup.destroy)
            vas1.pack(fill="both", expand=True)

            frame.pack()

            # Button Flow Control ..........

        def button_mode(selection, opt):
            """
            Module takes input as selction and opt to determine which button
            has been pressed.

            @param selection: choice of button group
            @param opt: choice in button group

            @rtype: None

            """

            if selection == 1:  # Winder Button Pressed
                choice[0] = 'WINDER'
                choice[1] = ''
                choice[2] = ''
                self.vas1.config(state=NORMAL, fg='white')
                self.vas2.config(state=NORMAL, fg='white')
                self.drive1.config(state=DISABLED)
                self.drive2.config(state=DISABLED)
                self.drive3.config(state=DISABLED)
                self.drive4.config(state=DISABLED)
                self.drive5.config(state=DISABLED)
                self.power.config(disabledforeground='gray')
                self.read.config(state=DISABLED)
                self.write.config(state=DISABLED)
                self.rabbit.grid(row=4, column=6, rowspan=1,
                                 columnspan=2, sticky=N + E + W + S)

            elif selection == 2:  # Unwinder Button Pressed
                choice[0] = 'UNWINDER'
                choice[1] = ''
                choice[2] = ''
                self.vas1.config(state=DISABLED, disabledforeground='gray')
                self.vas2.config(state=DISABLED, disabledforeground='gray')
                self.drive1.config(state=NORMAL)
                self.drive2.config(state=NORMAL)
                self.drive3.config(state=NORMAL)
                self.drive4.config(state=NORMAL)
                self.drive5.config(state=NORMAL)
                self.power.config(disabledforeground='white')
                self.read.config(state=DISABLED)
                self.write.config(state=DISABLED)
                self.rabbit.grid(row=5, column=6, rowspan=5,
                                 columnspan=2, sticky=N + E + W + S)

            elif selection == 3:  # Buffer Button Pressed
                choice[0] = 'BUFFER'
                choice[1] = ''
                choice[2] = ''
                self.vas1.config(state=DISABLED, disabledforeground='gray')
                self.vas2.config(state=DISABLED, disabledforeground='gray')
                self.drive1.config(state=DISABLED)
                self.drive2.config(state=DISABLED)
                self.drive3.config(state=DISABLED)
                self.drive4.config(state=DISABLED)
                self.drive5.config(state=DISABLED)
                self.power.config(disabledforeground='gray')
                self.read.config(state=NORMAL)
                self.write.config(state=NORMAL)
                self.rabbit.grid(row=10, column=6, rowspan=2,
                                 columnspan=2, sticky=N + E + W + S)

            elif selection == 4:  # Vas1 or Vas2 Button Pressed
                self.vas1.config(state=DISABLED, disabledforeground='gray')
                self.vas2.config(state=DISABLED, disabledforeground='gray')
                self.drive1.config(state=NORMAL)
                self.drive2.config(state=NORMAL)
                self.drive3.config(state=NORMAL)
                self.drive4.config(state=NORMAL)
                self.drive5.config(state=NORMAL)
                self.power.config(disabledforeground='white')
                self.rabbit.grid(row=5, column=6, rowspan=5,
                                 columnspan=2, sticky=N + E + W + S)

                if opt == 1:
                    choice[1] = ' . VAS1'
                else:
                    choice[1] = ' . VAS2'

            elif selection == 5:  # Drive 1,2,3,4 or 5 Button Pressed
                self.read.config(state=NORMAL, fg='white')
                self.write.config(state=NORMAL, fg='white')
                self.drive1.config(
                    state=DISABLED, disabledforeground='gray')
                self.drive2.config(
                    state=DISABLED, disabledforeground='gray')
                self.drive3.config(
                    state=DISABLED, disabledforeground='gray')
                self.drive4.config(
                    state=DISABLED, disabledforeground='gray')
                self.drive5.config(
                    state=DISABLED, disabledforeground='gray')
                self.power.config(disabledforeground='gray')
                self.rabbit.grid(row=10, column=6, rowspan=2,
                                 columnspan=2, sticky=N + E + W + S)

                if opt == 3:
                    choice[2] = ' . DRIVE1'
                if opt == 4:
                    choice[2] = ' . DRIVE2'
                if opt == 6:
                    choice[2] = ' . DRIVE3'
                if opt == 7:
                    choice[2] = ' . DRIVE4'
                if opt == 8:
                    choice[2] = ' . DRIVE5'
            else:
                self.rabbit.grid(row=1, column=6, rowspan=3,
                                 columnspan=2, sticky=N + E + W + S)

            self.info.config(text=choice[0] + choice[1] + choice[2])

        # Buttons start here

        # Top Labels ..........

        self.help = Button(self, text='HELP', bg='gray',
                           font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                           borderwidth=3, relief=RIDGE, activebackground='gray',
                           command=lambda: help())
        self.help.grid(row=0, column=0, columnspan=1,
                       sticky=N + E + W + S)

        self.heading = Label(self, text='SOCAPEL LOADER SOFTWARE by TGIPD',
                             font=('Times', '18', 'bold'), padx=0, pady=0, width=1,
                             bg='gray', fg='white', borderwidth=3, relief=RIDGE)
        self.heading.grid(row=0, column=1, rowspan=1,
                          columnspan=4, sticky=N + E + W + S)

        # Hidden Quit Button - Top Right ..........
        self.quit = Button(self, text='QUIT', fg='black',
                           bg='gray', font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                           borderwidth=3, relief=RIDGE, activebackground='gray',
                           command=lambda: root.destroy())

        self.quit.grid(row=0, column=5, rowspan=1,
                       columnspan=1, sticky=N + E + W + S)

        # Row ONE Buttons
        self.winder = Button(self, text='WINDER',
                             bg='DodgerBlue2', fg='black', font=('Times', '16', 'bold'),
                             padx=0, pady=0, width=1, borderwidth=3, relief=RIDGE,
                             activebackground='DodgerBlue3', command=lambda: button_mode(1, 0))

        self.winder.grid(row=1, column=0, rowspan=3,
                         columnspan=2, sticky=N + E + W + S)

        self.unwinder = Button(self, text='UNWINDER',
                               bg='DodgerBlue2', fg='black', font=('Times', '16', 'bold'),
                               padx=0, pady=0, width=1, borderwidth=3, relief=RIDGE,
                               activebackground='DodgerBlue3', command=lambda: button_mode(2, 0))
        self.unwinder.grid(row=1, column=2, rowspan=3,
                           columnspan=2, sticky=N + E + W + S)

        self.vsp = Button(self, text='BUFFER',
                          bg='DodgerBlue2', fg='black', font=('Times', '16', 'bold'),
                          padx=0, pady=0, width=1, borderwidth=3, relief=RIDGE,
                          activebackground='DodgerBlue3', command=lambda: button_mode(3, 0))
        self.vsp.grid(row=1, column=4, rowspan=3,
                      columnspan=2, sticky=N + E + W + S)

        self.rabbit = Label(self, text='\u23f4',
                            bg='black', fg='white', font=('Times', '20', 'bold'),
                            padx=0, pady=0, width=1, borderwidth=3, relief=RIDGE)

        self.rabbit.grid(row=1, column=6, rowspan=3,
                         columnspan=2, sticky=N + E + W + S)

        # Row TWO Buttons
        self.vas1 = Button(self, text='VAS1', bg='MediumPurple2',
                           font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                           borderwidth=3, relief=RIDGE, activebackground='MediumPurple3',
                           state=DISABLED, command=lambda: [button_mode(4, 1)])
        self.vas1.grid(row=4, column=0, columnspan=2, sticky=N + E + W + S)

        self.vas2 = Button(self, text='VAS2', bg='MediumPurple2',
                           font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                           borderwidth=3, relief=RIDGE, activebackground='MediumPurple3',
                           state=DISABLED, command=lambda: button_mode(4, 2))
        self.vas2.grid(row=4, column=2, columnspan=2, sticky=N + E + W + S)

        self.info = Label(self, text='', bg='MediumPurple2',
                          font=('Times', '10'), padx=0, pady=0, width=1, borderwidth=3,
                          relief=RIDGE)
        self.info.grid(row=4, column=4, columnspan=2,
                       sticky=N + E + W + S)

        # Row THREE Buttons, borderwidth=5
        self.drive1 = Button(self, text='DRIVE1', bg='orange2', fg='white',
                             font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                             borderwidth=3, relief=RIDGE, activebackground='orange3',
                             state=DISABLED, command=lambda: button_mode(5, 3))
        self.drive1.grid(row=5, column=0, rowspan=5,
                         sticky=N + E + W + S)

        self.drive2 = Button(self, text='DRIVE2', bg='orange2', fg='white',
                             font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                             borderwidth=3, relief=RIDGE, activebackground='orange3',
                             state=DISABLED, command=lambda: button_mode(5, 4))
        self.drive2.grid(row=5, column=1, rowspan=5,
                         sticky=N + E + W + S)

        self.power = Button(self, text='POWER', bg='orange2', fg='white',
                            font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                            borderwidth=3, relief=RIDGE, activebackground='orange3',
                            state=DISABLED, command=lambda: button_mode(5, 5))
        self.power.grid(row=5, column=2, rowspan=5, sticky=N + E + W + S)

        self.drive3 = Button(self, text='DRIVE3', bg='orange2', fg='white',
                             font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                             borderwidth=3, relief=RIDGE, activebackground='orange3',
                             state=DISABLED, command=lambda: button_mode(5, 6))
        self.drive3.grid(row=5, column=3, rowspan=5, sticky=N + E + W + S)

        self.drive4 = Button(self, text='DRIVE4', bg='orange2', fg='white',
                             font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                             borderwidth=3, relief=RIDGE, activebackground='orange3',
                             state=DISABLED, command=lambda: button_mode(5, 7))
        self.drive4.grid(row=5, column=4, rowspan=5, sticky=N + E + W + S)

        self.drive5 = Button(self, text='DRIVE5', bg='orange2', fg='white',
                             font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                             borderwidth=3, relief=RIDGE, activebackground='orange3',
                             state=DISABLED, command=lambda: button_mode(5, 8))
        self.drive5.grid(row=5, column=5, rowspan=5, sticky=N + E + W + S)

        # Row FOUR Buttons
        self.write = Button(self, text='WRITE TO SOCAPEL',
                            bg='green4', font=('Times', '16', 'bold'), padx=0, pady=0,
                            width=1, borderwidth=3, relief=RIDGE, activebackground='darkgreen',
                            state=DISABLED, command=lambda: button_mode(9, 9))
        self.write.grid(row=10, column=0, rowspan=2,
                        columnspan=5, sticky=N + E + W + S)

        self.read = Button(self, text='READ',
                           bg='red2', font=('Times', '16', 'bold'), padx=0, pady=0, width=1,
                           borderwidth=3, relief=RIDGE, activebackground='white',
                           state=DISABLED, command=lambda: button_mode(9, 9))

        self.read.grid(row=10, column=5, rowspan=2,
                       columnspan=1, sticky=N + E + W + S)


def main(root):
    my_gui = Application(root)
    com = Communication()
    root.mainloop()


if __name__ == '__main__':
    root = Tk()
    main(root)
