import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import sys


try:
    from huffman import LSBDetector, EsteganografiaLSB, CodificadorHuffman
except ImportError:
    messagebox.showerror("Error", "No se encontró el archivo huffman.py en el mismo directorio")
    sys.exit(1)


class LSBDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector LSB con Compresión Huffman")
        self.root.geometry("900x700")
        self.root.configure(bg='#2b2b2b')
       
        self.detector = LSBDetector()
        self.estego = EsteganografiaLSB()
        
        self.imagen_seleccionada = None
        self.imagen_entrada = None
        
        self.setup_ui()
    
    def setup_ui(self):
        
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_dark = '#2b2b2b'
        bg_medium = '#3d3d3d'
        fg_light = '#ffffff'
        accent_purple = '#c77dff'
        accent_cyan = '#4cc9f0'
        
        style.configure('TFrame', background=bg_dark)
        style.configure('Title.TLabel', background=bg_dark, foreground=fg_light, font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_dark, foreground=accent_cyan, font=('Segoe UI', 11, 'bold'))
        style.configure('Info.TLabel', background=bg_dark, foreground=fg_light, font=('Segoe UI', 10))
        style.configure('TButton', background=accent_purple, foreground=fg_light, font=('Segoe UI', 10), borderwidth=0, focuscolor='none')
        style.map('TButton', background=[('active', '#9d4edd')])
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        

        title_label = ttk.Label(main_frame, text="Detector LSB ", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.setup_tab_analizar()
        self.setup_tab_crear()
        self.setup_tab_ocultar()
        self.setup_tab_huffman()
        
    def setup_tab_analizar(self):
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Realizar Análisis")
        
        select_frame = ttk.Frame(tab, padding="10")
        select_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(select_frame, text="Seleccionar imagen:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(select_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.btn_seleccionar = self.create_button(btn_frame, "📁 Seleccionar Imagen", 
                                                   self.seleccionar_imagen_analizar)
        self.btn_seleccionar.pack(side=tk.LEFT, padx=5)
        
        self.label_imagen_analizar = ttk.Label(select_frame, text="Ninguna imagen seleccionada", 
                                               style='Info.TLabel')
        self.label_imagen_analizar.pack(anchor=tk.W, pady=5)
        
        analysis_frame = ttk.Frame(tab, padding="10")
        analysis_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(analysis_frame, text="Métodos de extracción:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W)
        
        btn_frame2 = ttk.Frame(analysis_frame)
        btn_frame2.pack(fill=tk.X, pady=5)
        
        self.create_button(btn_frame2, "Análisis Completo",
                          self.analizar_completo).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame2, "Fuerza Bruta", 
                          lambda: self.extraer_mensaje('fuerza_bruta')).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame2, "Divide y Vencerás", 
                          lambda: self.extraer_mensaje('divide_y_venceras')).pack(side=tk.LEFT, padx=5)
        
        results_frame = ttk.Frame(tab, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(results_frame, text="Resultados:", 
                 style='Subtitle.TLabel').pack(anchor=tk.W)
        
        self.text_resultados = scrolledtext.ScrolledText(results_frame, 
                                                         bg='#1e1e1e', 
                                                         fg='#ffffff',
                                                         font=('Consolas', 10),
                                                         height=15)
        self.text_resultados.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def setup_tab_crear(self):

        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="➕ Crear Imagen")
        
        content_frame = ttk.Frame(tab, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Crear una nueva imagen con mensaje oculto", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        ttk.Label(content_frame, text="Mensaje a ocultar:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_mensaje_crear = tk.Text(content_frame, height=4, 
                                           bg='#1e1e1e', fg='#ffffff',
                                           font=('Segoe UI', 10))
        self.entry_mensaje_crear.pack(fill=tk.X, pady=5)
       
        ttk.Label(content_frame, text="Nombre del archivo:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_nombre_crear = ttk.Entry(content_frame)
        self.entry_nombre_crear.insert(0, "img_con_mensaje.png")
        self.entry_nombre_crear.pack(fill=tk.X, pady=5)
    
        self.create_button(content_frame, "Crear Imagen", 
                          self.crear_imagen).pack(pady=20)
    
    def setup_tab_ocultar(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Ocultar Estándar")
        
        content_frame = ttk.Frame(tab, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Ocultar mensaje (LSB estándar) en imagen existente", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.create_button(btn_frame, "📁 Seleccionar Imagen", 
                          self.seleccionar_imagen_ocultar).pack(side=tk.LEFT, padx=5)
        
        self.label_imagen_ocultar = ttk.Label(content_frame, 
                                             text="Ninguna imagen seleccionada", 
                                             style='Info.TLabel')
        self.label_imagen_ocultar.pack(anchor=tk.W, pady=5)
        
        ttk.Label(content_frame, text="Mensaje a ocultar:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_mensaje_ocultar = tk.Text(content_frame, height=4, 
                                            bg='#1e1e1e', fg='#ffffff',
                                            font=('Segoe UI', 10))
        self.entry_mensaje_ocultar.pack(fill=tk.X, pady=5)
        

        ttk.Label(content_frame, text="Nombre del archivo de salida:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_salida_ocultar = ttk.Entry(content_frame)
        self.entry_salida_ocultar.insert(0, "img_mensaje.png")
        self.entry_salida_ocultar.pack(fill=tk.X, pady=5)
        
    
        self.create_button(content_frame, "🔒 Ocultar Mensaje", 
                          self.ocultar_mensaje).pack(pady=20)
    
    def setup_tab_huffman(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Ocultar con Huffman")
        
        content_frame = ttk.Frame(tab, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Ocultar mensaje con compresión Huffman", 
                 style='Subtitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.create_button(btn_frame, "📁 Seleccionar Imagen", 
                          self.seleccionar_imagen_huffman).pack(side=tk.LEFT, padx=5)
        
        self.label_imagen_huffman = ttk.Label(content_frame, 
                                             text="Ninguna imagen seleccionada", 
                                             style='Info.TLabel')
        self.label_imagen_huffman.pack(anchor=tk.W, pady=5)
        
        ttk.Label(content_frame, text="Mensaje a ocultar:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_mensaje_huffman = tk.Text(content_frame, height=4, 
                                            bg='#1e1e1e', fg='#ffffff',
                                            font=('Segoe UI', 10))
        self.entry_mensaje_huffman.pack(fill=tk.X, pady=5)
        

        canal_frame = ttk.Frame(content_frame)
        canal_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(canal_frame, text="Canal:", style='Info.TLabel').pack(side=tk.LEFT, padx=5)
        self.canal_var = tk.StringVar(value="0")
        
        ttk.Radiobutton(canal_frame, text="Rojo (0)", variable=self.canal_var, 
                       value="0").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(canal_frame, text="Verde (1)", variable=self.canal_var, 
                       value="1").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(canal_frame, text="Azul (2)", variable=self.canal_var, 
                       value="2").pack(side=tk.LEFT, padx=5)
        
        ttk.Label(content_frame, text="Nombre del archivo de salida:", 
                 style='Info.TLabel').pack(anchor=tk.W, pady=(10, 5))
        self.entry_salida_huffman = ttk.Entry(content_frame)
        self.entry_salida_huffman.insert(0, "img_huffman.png")
        self.entry_salida_huffman.pack(fill=tk.X, pady=5)
    
        self.create_button(content_frame, "Ocultar con Huffman", 
                          self.ocultar_huffman).pack(pady=20)
    
    def create_button(self, parent, text, command):
    
        btn = tk.Button(parent, text=text, command=command,
                       bg='#c77dff', fg='#ffffff',
                       font=('Segoe UI', 10, 'bold'),
                       relief=tk.FLAT, padx=20, pady=10,
                       cursor='hand2')
        btn.bind('<Enter>', lambda e: btn.config(bg='#9d4edd'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#c77dff'))
        return btn
    
    
    
    def seleccionar_imagen_analizar(self):
        
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if filename:
            self.imagen_seleccionada = filename
            self.label_imagen_analizar.config(text=f"📄 {Path(filename).name}")
    
    def seleccionar_imagen_ocultar(self):
        
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if filename:
            self.imagen_entrada = filename
            self.label_imagen_ocultar.config(text=f"📄 {Path(filename).name}")
    
    def seleccionar_imagen_huffman(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        if filename:
            self.imagen_entrada = filename
            self.label_imagen_huffman.config(text=f"📄 {Path(filename).name}")
    
    def log_resultado(self, mensaje):
        self.text_resultados.insert(tk.END, mensaje + "\n")
        self.text_resultados.see(tk.END)
        self.root.update()
    
    def analizar_completo(self):
        if not self.imagen_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una imagen primero")
            return
        
        self.text_resultados.delete(1.0, tk.END)
        self.log_resultado("="*60)
        self.log_resultado("INICIANDO ANÁLISIS...")
        self.log_resultado("="*60)
        
        def analizar_thread():
            try:
                import sys
                from io import StringIO
                
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                self.detector.analizar_imagen_completo(self.imagen_seleccionada)
                
                output = sys.stdout.getvalue()
                sys.stdout = old_stdout
                
                self.root.after(0, lambda: self.log_resultado(output))
                self.root.after(0, lambda: messagebox.showinfo("Completado", 
                                                               "Análisis completado"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        threading.Thread(target=analizar_thread, daemon=True).start()
    
    def extraer_mensaje(self, metodo):
        if not self.imagen_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una imagen primero")
            return
        
        self.text_resultados.delete(1.0, tk.END)
        self.log_resultado(f"Extrayendo con {metodo}...")
        
        mensaje = self.detector.extraer_mensaje_lsb(self.imagen_seleccionada, metodo)
        
        if mensaje:
            self.log_resultado(f"\nMensaje encontrado: '{mensaje}'")
            messagebox.showinfo("Éxito", f"Mensaje: {mensaje}")
        else:
            self.log_resultado("\nNo se encontró mensaje")
            messagebox.showinfo("Resultado", "No se encontró mensaje oculto")
    
    def crear_imagen(self):
        mensaje = self.entry_mensaje_crear.get(1.0, tk.END).strip()
        nombre = self.entry_nombre_crear.get().strip()
        
        if not mensaje:
            messagebox.showwarning("Advertencia", "Ingresa un mensaje")
            return
        
        if not nombre:
            nombre = "imagen_con_mensaje.png"
        
        if self.estego.crear_imagen_con_mensaje(mensaje, nombre):
            messagebox.showinfo("Éxito", f"Imagen creada: {nombre}")
        else:
            messagebox.showerror("Error", "No se pudo crear la imagen")
    
    def ocultar_mensaje(self):
        if not self.imagen_entrada:
            messagebox.showwarning("Advertencia", "Selecciona una imagen primero")
            return
        
        mensaje = self.entry_mensaje_ocultar.get(1.0, tk.END).strip()
        salida = self.entry_salida_ocultar.get().strip()
        
        if not mensaje:
            messagebox.showwarning("Ingresa un mensaje")
            return
        
        if not salida:
            salida = "imagen_estego.png"
        
        if self.estego.ocultar_mensaje_en_imagen_existente(mensaje, self.imagen_entrada, salida):
            messagebox.showinfo("Éxito", f"Mensaje oculto en: {salida}")
        else:
            messagebox.showerror("Error", "No se pudo ocultar el mensaje")
    
    def ocultar_huffman(self):
        if not self.imagen_entrada:
            messagebox.showwarning("Advertencia", "Selecciona una imagen primero")
            return
        
        mensaje = self.entry_mensaje_huffman.get(1.0, tk.END).strip()
        salida = self.entry_salida_huffman.get().strip()
        canal = int(self.canal_var.get())
        
        if not mensaje:
            messagebox.showwarning("Advertencia", "Ingresa un mensaje")
            return
        
        if not salida:
            salida = "imagen_huffman_estego.png"
        
        if self.detector.ocultar_mensaje_huffman(self.imagen_entrada, mensaje, salida, canal):
            messagebox.showinfo("Éxito", f"Mensaje oculto con Huffman en: {salida}")
        else:
            messagebox.showerror("Error", "No se pudo ocultar el mensaje")


def main():
    root = tk.Tk()
    app = LSBDetectorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()