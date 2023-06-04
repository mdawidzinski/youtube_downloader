import tkinter as tk
from tkinter import ttk


def add_link():
    link = entry.get()
    entry.delete(0, tk.END)
    if link not in archival_links:
        archival_links.append(link)
        if len(archival_links) > 10:
            archival_links.pop(0)
    combobox["values"] = archival_links


def select_link(event):
    selected_link = combobox.get()
    entry.delete(0, tk.END)
    entry.insert(0, selected_link)


root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Dodaj link", command=add_link)
button.pack()

archival_links = []  # Lista przechowująca ostatnie 10 wprowadzonych linków

combobox = ttk.Combobox(root, values=archival_links)
combobox.pack()
combobox.bind("<<ComboboxSelected>>", select_link)

root.mainloop()
