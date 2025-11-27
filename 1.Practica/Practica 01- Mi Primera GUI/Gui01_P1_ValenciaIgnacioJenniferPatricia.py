import tkinter as tk  

root = tk.Tk()
root.title("GUI")
root.geometry("550x400")

lbl = tk.Label(root, text="Hola, Bienvenido a mi GUI!")
lbl.pack(pady=25)

lbl = tk.Label(root, text="ay y eso")
lbl.pack(pady=15)


root.mainloop()
