#!/usr/bin/env python
#
# Copyright 2010 Ettus Research LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import usrp2_card_burner #import implementation
import Tkinter, Tkconstants, tkFileDialog, tkFont, tkMessageBox
import os

class BinFileEntry(Tkinter.Frame):
    """
    Simple file entry widget for getting the file path of bin files.
    Combines a label, entry, and button with file dialog callback.
    """

    def __init__(self, root, what, def_path=''):
        self._what = what
        Tkinter.Frame.__init__(self, root)
        Tkinter.Label(self, text=what+":").pack(side=Tkinter.LEFT)
        self._entry = Tkinter.Entry(self, width=50)
        self._entry.insert(Tkinter.END, def_path)
        self._entry.pack(side=Tkinter.LEFT)
        Tkinter.Button(self, text="...", command=self._button_cb).pack(side=Tkinter.LEFT)

    def _button_cb(self):
        filename = tkFileDialog.askopenfilename(
            parent=self,
            filetypes=[('bin files', '*.bin'), ('all files', '*.*')],
            title="Select bin file for %s"%self._what,
            initialdir=os.path.dirname(self.get_filename()),
        )

        # open file on your own
        if filename:
            self._entry.delete(0, Tkinter.END)
            self._entry.insert(0, filename)

    def get_filename(self):
        return self._entry.get()

class DeviceEntryWidget(Tkinter.Frame):
    """
    Simple  entry widget for getting the raw device name.
    Combines a label, entry, and helpful text box with hints.
    """

    def __init__(self, root, text=''):
        Tkinter.Frame.__init__(self, root)

        Tkinter.Button(self, text="Rescan for Devices", command=self._reload_cb).pack()

        self._hints = Tkinter.Listbox(self)
        self._hints.bind("<<ListboxSelect>>", self._listbox_cb)
        self._reload_cb()
        self._hints.pack(expand=Tkinter.YES, fill=Tkinter.X)

        frame = Tkinter.Frame(self)
        frame.pack()

        Tkinter.Label(frame, text="Raw Device:").pack(side=Tkinter.LEFT)
        self._entry = Tkinter.Entry(frame, width=50)
        self._entry.insert(Tkinter.END, text)
        self._entry.pack(side=Tkinter.LEFT)

    def _reload_cb(self):
        self._hints.delete(0, Tkinter.END)
        for hint in usrp2_card_burner.get_raw_device_hints():
            self._hints.insert(Tkinter.END, hint)

    def _listbox_cb(self, event):
        try:
            sel = self._hints.get(self._hints.curselection()[0])
            self._entry.delete(0, Tkinter.END)
            self._entry.insert(0, sel)
        except Exception, e: print e

    def get_devname(self):
        return self._entry.get()

class SectionLabel(Tkinter.Label):
    """
    Make a text label with bold font.
    """

    def __init__(self, root, text):
        Tkinter.Label.__init__(self, root, text=text)

        #set the font bold
        f = tkFont.Font(font=self['font'])
        f['weight'] = 'bold'
        self['font'] = f.name

class USRP2CardBurnerApp(Tkinter.Frame):
    """
    The top level gui application for the usrp2 sd card burner.
    Creates entry widgets and button with callback to write images.
    """

    def __init__(self, root, dev, fw, fpga):

        Tkinter.Frame.__init__(self, root)

        #pack the file entry widgets
        SectionLabel(self, text="Select Images").pack(pady=5)
        self._fw_img_entry = BinFileEntry(self, "Firmware Image", def_path=fw)
        self._fw_img_entry.pack()
        self._fpga_img_entry = BinFileEntry(self, "FPGA Image", def_path=fpga)
        self._fpga_img_entry.pack()

        #pack the destination entry widget
        SectionLabel(self, text="Select Device").pack(pady=5)
        self._raw_dev_entry = DeviceEntryWidget(self, text=dev)
        self._raw_dev_entry.pack()

        #the do it button
        SectionLabel(self, text="").pack(pady=5)
        Tkinter.Label(self, text="Warning! This tool can overwrite your hard drive. Use with caution.").pack()
        Tkinter.Button(self, text="Burn SD Card", command=self._burn).pack()

    def _burn(self):
        #grab strings from the gui
        fw = self._fw_img_entry.get_filename()
        fpga = self._fpga_img_entry.get_filename()
        dev = self._raw_dev_entry.get_devname()

        #check input
        if not dev:
            tkMessageBox.showerror('Error:', 'No device specified!')
            return
        if not fw and not fpga:
            tkMessageBox.showerror('Error:', 'No images specified!')
            return
        if fw and not os.path.exists(fw):
            tkMessageBox.showerror('Error:', 'Firmware image not found!')
            return
        if fpga and not os.path.exists(fpga):
            tkMessageBox.showerror('Error:', 'FPGA image not found!')
            return

        #burn the sd card
        try:
            verbose = usrp2_card_burner.burn_sd_card(dev=dev, fw=fw, fpga=fpga)
            tkMessageBox.showinfo('Verbose:', verbose)
        except Exception, e:
            tkMessageBox.showerror('Verbose:', 'Error: %s'%str(e))

########################################################################
# main
########################################################################
if __name__=='__main__':
    options = usrp2_card_burner.get_options()
    root = Tkinter.Tk()
    root.title('USRP2 SD Card Burner')
    USRP2CardBurnerApp(root, dev=options.dev, fw=options.fw, fpga=options.fpga).pack()
    root.mainloop()
    exit()
