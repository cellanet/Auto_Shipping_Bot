import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from OpenERP import driver
from threading import *
from SoapShip import UPS_API
from SoapReship import UPS_reprint_label
from SoapVoid import UPS_Void

running = True

def loop_thread():
    if running:  # Only do this if the Stop button has not been clicked
        #UPS_API()
        thread = Thread(target=UPS_API)
        thread.daemon = True
        thread.start()
    root.after(295000, loop_thread) # 5 mins cycle = 295000

def jump_start():
    root.after(1000, loop_thread())
    start.grid_remove()
    labelText.set('Running')

def startt():
    global running
    running = True
    labelText.set('Running')

def stop():
    #print("stop")
    global running
    running = False
    labelText.set('Idle')

def open_popup(string):
    win = tk.Toplevel()
    win.wm_title("Status")

    l = tk.Label(win, text=string)
    l.grid(row=0, column=0)

    pop_button = ttk.Button(win, text="OK.", command=win.destroy)
    pop_button.grid(row=1, column=0)

def reprint_label():
    msg = UPS_reprint_label(input_tracking.get())
    open_popup(msg)
def void_label():
    msg = UPS_Void(input_tracking.get())
    open_popup(msg)

def addItemToList(file, item):
    item = item.lower()
    if file == 'Item':
        f = open('item_list.txt', 'a')
        f.write(f'\n{item}')
        f.close()
    elif file == 'Attach':
        f = open('attachment.txt', 'a')
        f.write(f'\n{item}')
        f.close()

def update():
    f1 = open('item_list.txt', 'r')
    item_list = f1.readlines()
    f1.close()

    item_list.append('\n\n============== attach ==============\n\n')

    f2 = open('attachment.txt', 'r')
    attachments = f2.readlines()
    f2.close()

    allItem = item_list + attachments

    list_var =  StringVar(value=allItem)

    win = tk.Toplevel()
    win.wm_title(f"All Items")
    listbox = tk.Listbox(win, listvariable=list_var, height=30, width=30, selectmode='extended')

    scrollbar = ttk.Scrollbar(win, orient='vertical', command=listbox.yview)
    scrollbar.grid(row=0, column=1, sticky=tk.NS)
    listbox.config(yscrollcommand= scrollbar.set)
    listbox.grid(column=0, row=0, sticky='nwes')



def addItem(file):
    win = tk.Toplevel()
    win.wm_title(f"Add New {file}")

    item = Entry(win, width=20, justify='center')
    item.grid(row=0, column=0, pady=5, columnspan=2, padx=5)

    submit_button = ttk.Button(win, text="Submit", command=lambda: [addItemToList(file, item.get()), item.delete(0, 'end')])
    submit_button.grid(row=1, column=0, pady=5, padx=5, sticky='ew')

    pop_button = ttk.Button(win, text="Close", command=win.destroy)
    pop_button.grid(row=1, column=1, pady=5, padx=5, sticky='ew')


root = tk.Tk()
root.title('ULO Shipping')
canvas = tk.Canvas(root, width=80, height=50)
root.resizable(False, False)
canvas.grid(columnspan=3, rowspan=3)
root.grid_columnconfigure(0, weight=0)
root.grid_rowconfigure(0, weight=0)

#theme
style = ttk.Style(root)
root.tk.call('source', 'forest-light.tcl')
style.theme_use('forest-light')

#menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add Item", command=lambda: addItem('Item'))
filemenu.add_command(label="Add Attachment", command=lambda: addItem('Attach'))
filemenu.add_command(label="Show Items List", command=update)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


# Tabs
tab = ttk.Notebook(root)
shipping_tab = ttk.Frame(tab)
print = ttk.Frame(tab)
void = ttk.Frame(tab)

tab.add(shipping_tab, text="Ship", compound=TOP)
tab.add(print, text="UPS")
tab.add(void, text="USPS")
tab.grid(row=0, column=0, sticky='E', padx=0)

#=============================== Shipping Tab ==================================
labelText = StringVar()
resume = Button(shipping_tab, text='Resume', command=startt)  # , command=start_thread    , bg='#448551'
resume.grid(column=0, row=1, padx=8, pady=15, sticky='ew')
stopp = Button(shipping_tab, text='  Stop  ', command=stop)
stopp.grid(column=2, row=1, padx=5, pady=15, sticky='ew')
start = Button(shipping_tab, text='  Start  ', command=jump_start)
start.grid(column=1, row=1, padx=5, pady=15, sticky='ew')
label = Label(root, textvariable=labelText)
label.config(font=("Comic Sans MS", 7)) #Segoe Script
label.grid(column=0, row=1)
labelText.set('Idle')

#================================================================================
#=============================== Re-print Tab ===================================
input_tracking = Entry(print, width=30)
input_tracking.grid(row=0, column=0, columnspan= 3)
rePrint = Button(print, text="Re-Print Label", command=reprint_label)
rePrint.grid(row=1, column=0, columnspan=2)
void_button = Button(print, text="Void", command= void_label)
void_button.grid(row=1, column=2, sticky='ew')
#================================================================================

canvas = tk.Canvas(root, width=10, height=10)
canvas.grid(columnspan=3)
root.config(menu=menubar)
root.mainloop()
driver.quit()