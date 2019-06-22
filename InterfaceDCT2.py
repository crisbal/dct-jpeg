from compress import do_compress
import os 
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter import StringVar, IntVar
from tkinter import messagebox

root = tk.Tk()
root.title('Compressione Immagini BMP')

root.resizable(False, False)
frame = tk.Frame(root)
frame.pack()

filename = StringVar()
F_value = StringVar()
F_value.set('8')
d_value = StringVar()
d_value.set('3')
full_filename = ""

def compress_image():
    file_path = full_filename
    if not file_path:
        messagebox.showerror("Errore", "Devi prima selezionare un file.")
        return

    F = F_value.get()
    if F and F.isdigit() and int(F) > 0:
        F = int(F)
    else:
        messagebox.showerror("Errore", "F deve essere un numero intero positivo.")
        return

    d = d_value.get()
    if d and d.isdigit():
        d = int(d)
        if d > (2*F-2):
            messagebox.showerror("Errore", f"d ({d}) deve essere compreso tra 0 e 2F-2 ({2*F-2}).")
            return
    else:
        messagebox.showerror("Errore", "d deve essere un numero intero e positivo.")
        return
    
    global compress_btn_text
    do_compress(file_path, F, d)

def choose_file():
    global full_filename
    file_path = askopenfilename(title='select new file', filetypes=[("BMP Image", "*.bmp")])
    if not file_path:
        return
    full_filename = file_path
    file_tree = file_path.split(os.sep)
    file_name = file_tree[-1]
    folder_name = file_tree[-2]
    filename.set(f'...{os.sep}{folder_name}{os.sep}{file_name}')


tk.Label(frame, text = "Scegli l'immagine BMP: ").grid(sticky="w", row=0, column=0, pady = 10, padx = 20)
tk.Entry(frame, width = 30, state='disabled', textvariable=filename).grid(row=0,column=1)
Button(frame, text="Scegli", 
            command=choose_file).grid(row=0, column=2, pady = 10, padx = 20)

tk.Label(frame, text = "Inserisci il valore di F:\nF > 0").grid(sticky="w",row=1, column=0, pady = 10, padx = 20)
tk.Entry(frame, width = 30, textvariable=F_value, justify='center').grid(row=1, column=1, pady = 10, padx = 0)

tk.Label(frame, text = "Inserisci il valore di d:\n0 <= d <= 2F-2").grid(sticky="w",row=2, column=0, pady = 10, padx = 20)
tk.Entry(frame, width = 30, textvariable=d_value, justify='center').grid(row=2, column=1, pady = 10, padx = 0)

btn = tk.Button(frame, 
            text="Comprimi immagine", font="-weight bold",
            command=compress_image).grid(row=4, column=0, columnspan = 3, pady = 10, padx = 20, sticky = tk.W+tk.E)

tk.mainloop()
