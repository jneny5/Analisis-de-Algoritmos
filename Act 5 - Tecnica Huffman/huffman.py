import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import heapq, json, os, math

class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def contar_frecuencias(texto):
    freqs = {}
    for c in texto:
        freqs[c] = freqs.get(c, 0) + 1
    return freqs

def construir_arbol(freqs):
    heap = []
    for ch, f in freqs.items():
        heapq.heappush(heap, (f, HuffmanNode(f, char=ch)))
    if len(heap) == 0:
        return None
    
    if len(heap) == 1:
        f, node = heapq.heappop(heap)
        root = HuffmanNode(f, left=node, right=None)
        return root
    while len(heap) > 1:
        f1, n1 = heapq.heappop(heap)
        f2, n2 = heapq.heappop(heap)
        merged = HuffmanNode(f1+f2, left=n1, right=n2)
        heapq.heappush(heap, (merged.freq, merged))
    return heapq.heappop(heap)[1]

def generar_codigos(root):
    codes = {}
    def dfs(node, pref):
        if node is None:
            return
        if node.char is not None and node.left is None and node.right is None:
            codes[node.char] = pref or "0"
            return
        dfs(node.left, pref + "0")
        dfs(node.right, pref + "1")
    dfs(root, "")
    return codes

def bits_a_bytes(bitstring):
    b = bytearray()
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        b.append(int(byte, 2))
    return bytes(b)

def bytes_a_bits(b):
    return "".join(f"{byte:08b}" for byte in b)

def guardar_comprimido(ruta_bin, bitstring):
    pad_len = (8 - len(bitstring) % 8) % 8
    bitstring_padded = bitstring + ("0" * pad_len)
    data = bits_a_bytes(bitstring_padded)
    with open(ruta_bin, "wb") as f:
        f.write(bytes([pad_len]))   
        f.write(data)

def leer_comprimido(ruta_bin):
    with open(ruta_bin, "rb") as f:
        pad_len_byte = f.read(1)
        if not pad_len_byte:
            return ""
        pad_len = pad_len_byte[0]
        data = f.read()
    bitstring = bytes_a_bits(data)
    if pad_len:
        bitstring = bitstring[:-pad_len]
    return bitstring

def codificar_texto(texto, codes):
    return "".join(codes[ch] for ch in texto)

def decodificar_bits(bitstring, codes):
   
    inv = {v: k for k, v in codes.items()}
    decoded_chars = []
    cur = ""
    for bit in bitstring:
        cur += bit
        if cur in inv:
            decoded_chars.append(inv[cur])
            cur = ""
    return "".join(decoded_chars)

#GUI 
class HuffmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Huffman Compressor")
        master.geometry("800x600")

        self.filepath = None
        self.texto = ""
        self.codes = {}
        self.bin_path = None

        frame_top = tk.Frame(master)
        frame_top.pack(pady=8)

        btn_open = tk.Button(frame_top, text="Abrir .txt", command=self.open_file)
        btn_open.grid(row=0, column=0, padx=6)

        btn_compress = tk.Button(frame_top, text="Comprimir", command=self.compress_file)
        btn_compress.grid(row=0, column=1, padx=6)

        btn_decompress = tk.Button(frame_top, text="Descomprimir", command=self.decompress_file)
        btn_decompress.grid(row=0, column=2, padx=6)

        btn_save_codes = tk.Button(frame_top, text="Guardar códigos (.json)", command=self.save_codes)
        btn_save_codes.grid(row=0, column=3, padx=6)

        btn_show_codes = tk.Button(frame_top, text="Ver códigos", command=self.show_codes)
        btn_show_codes.grid(row=0, column=4, padx=6)

        stats_frame = tk.Frame(master)
        stats_frame.pack(pady=6)
        self.lbl_stats = tk.Label(stats_frame, text="No hay archivo cargado")
        self.lbl_stats.pack()

        txt_frame = tk.Frame(master)
        txt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.txt_area = scrolledtext.ScrolledText(txt_frame, wrap=tk.WORD)
        self.txt_area.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if not fp:
            return
        self.filepath = fp
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            self.texto = f.read()
        self.txt_area.delete(1.0, tk.END)
        self.txt_area.insert(tk.END, self.texto[:10000]) 
        self.lbl_stats.config(text=f"Archivo: {os.path.basename(fp)}  |  Tamaño: {os.path.getsize(fp)} bytes")
        messagebox.showinfo("Archivo cargado", "Archivo cargado correctamente. Ahora puedes comprimirlo.")

    def compress_file(self):
        if not self.texto:
            messagebox.showwarning("Error", "Primero abre un archivo .txt")
            return
        freqs = contar_frecuencias(self.texto)
        root = construir_arbol(freqs)
        self.codes = generar_codigos(root)
        bitstring = codificar_texto(self.texto, self.codes)
        
        folder = filedialog.askdirectory(title="Carpeta para guardar resultados")
        if not folder:
            return
        base = os.path.splitext(os.path.basename(self.filepath))[0]
        bin_path = os.path.join(folder, base + "_compressed.bin")
        json_path = os.path.join(folder, base + "_codes.json")
        guardar_comprimido(bin_path, bitstring)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.codes, f, ensure_ascii=False)
        self.bin_path = bin_path
        orig_size = os.path.getsize(self.filepath)
        comp_size = os.path.getsize(bin_path) + os.path.getsize(json_path)
        saved = orig_size - comp_size
        pct = (1 - comp_size / orig_size) * 100 if orig_size>0 else 0
        self.lbl_stats.config(text=(
            f"Original: {orig_size} bytes  |  Comprimido+codes: {comp_size} bytes  |  "
            f"Ahorro: {saved} bytes ({pct:.2f}%)"
        ))
        messagebox.showinfo("Comprimido", f"Guardado: {bin_path}\nCódigos: {json_path}")

    def decompress_file(self):
        if not self.bin_path:
            bin_fp = filedialog.askopenfilename(title="Selecciona .bin", filetypes=[("BIN files","*.bin")])
            if not bin_fp:
                return
            self.bin_path = bin_fp
        else:
            bin_fp = self.bin_path
        codes_fp = filedialog.askopenfilename(title="Selecciona códigos (.json)", filetypes=[("JSON files","*.json")])
        if not codes_fp:
            return
        with open(codes_fp, "r", encoding="utf-8") as f:
            codes = json.load(f)
        bitstring = leer_comprimido(bin_fp)
        texto = decodificar_bits(bitstring, codes)
        
        folder = filedialog.askdirectory(title="Carpeta para guardar texto descomprimido")
        if not folder:
            return
        base = os.path.splitext(os.path.basename(bin_fp))[0]
        out_path = os.path.join(folder, base + "_decompressed.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(texto)
        messagebox.showinfo("Descomprimido", f"Descomprimido guardado en:\n{out_path}")
        self.txt_area.delete(1.0, tk.END)
        self.txt_area.insert(tk.END, texto[:10000])
        self.lbl_stats.config(text=f"Descomprimido: {out_path}  |  Tamaño: {len(texto.encode('utf-8'))} bytes")

    def save_codes(self):
        if not self.codes:
            messagebox.showwarning("Sin códigos", "No hay códigos generados. Primero comprime un archivo.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON",".json")])
        if not fp:
            return
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(self.codes, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Códigos guardados", f"Códigos guardados en {fp}")

    def show_codes(self):
        if not self.codes:
            messagebox.showwarning("Sin códigos", "No hay códigos generados.")
            return
        popup = tk.Toplevel(self.master)
        popup.title("Códigos Huffman")
        st = scrolledtext.ScrolledText(popup, width=60, height=30)
        st.pack(padx=10, pady=10)
        for ch, code in sorted(self.codes.items(), key=lambda x: (len(x[1]), x[0])):
            display_char = ch if ch != "\n" else "\\n"
            display_char = display_char if ch != " " else "' ' (space)"
            st.insert(tk.END, f"{repr(display_char)} : {code}\n")
        st.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()
