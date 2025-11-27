import tkinter as tk

def saludar():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "mundo"
    lbl.config(text=f"Holiiis, {nombre} 👋")

def cuenta():
    nombre = entrada.get().strip()
    if not nombre:
        nombre = "numero"
    lbl.config(text="Gracias por tu numero de cuentaa")

root = tk.Tk()
root.title("Saludador")
root.geometry("550x400")

lbl = tk.Label(root, text="Hola bienvenido, Escribe tu nombre y presiona el botón porfis")
lbl.pack(pady=10)

entrada = tk.Entry(root)
entrada.pack(pady=5)

btn = tk.Button(root, text="Next", command=saludar)
btn.pack(pady=10)

lbl = tk.Label(root, text="aver ahora tu numero de banco")
lbl.pack(pady=10)

entrada = tk.Entry(root)
entrada.pack(pady=5)

btn = tk.Button(root, text="date", command=cuenta)
btn.pack(pady=10)

btn = tk.Button(root, text="boton 3", command=cuenta)
btn.pack(pady=10)
btn = tk.Button(root, text="boton 4", command=cuenta)
btn.pack(pady=10)
btn = tk.Button(root, text="boton 5", command=cuenta)
btn.pack(pady=10)

root.mainloop()
