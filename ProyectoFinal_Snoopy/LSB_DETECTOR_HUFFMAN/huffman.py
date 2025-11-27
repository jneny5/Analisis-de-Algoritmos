import cv2
import numpy as np
from PIL import Image
from scipy import stats
import os
import glob
import time
import heapq
from collections import Counter
import json


class NodoHuffman:
    
    def __init__(self, caracter=None, frecuencia=0, izquierda=None, derecha=None):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = izquierda
        self.derecha = derecha
    
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
    
    def __eq__(self, otro):
        return self.frecuencia == otro.frecuencia


class CodificadorHuffman:
    
    def __init__(self):
        self.raiz = None
        self.codigos = {}
        self.codigos_inversos = {}
    
    def calcular_frecuencias(self, texto):
        return Counter(texto)
    
    def construir_arbol(self, frecuencias):
        if not frecuencias:
            return None
        heap = [NodoHuffman(caracter=car, frecuencia=freq) for car, freq in frecuencias.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)
            padre = NodoHuffman(frecuencia=izq.frecuencia + der.frecuencia, izquierda=izq, derecha=der)
            heapq.heappush(heap, padre)
        return heap[0] if heap else None
    
    def generar_codigos(self, nodo=None, codigo_actual=""):
        if nodo is None:
            nodo = self.raiz
            self.codigos = {}
            self.codigos_inversos = {}
        if nodo is None:
            return
        if nodo.caracter is not None:
            codigo = codigo_actual if codigo_actual else "0"
            self.codigos[nodo.caracter] = codigo
            self.codigos_inversos[codigo] = nodo.caracter
            return
        if nodo.izquierda:
            self.generar_codigos(nodo.izquierda, codigo_actual + "0")
        if nodo.derecha:
            self.generar_codigos(nodo.derecha, codigo_actual + "1")
    
    def codificar_texto(self, texto):
        if not texto:
            return "", {}, {}
        frecuencias = self.calcular_frecuencias(texto)
        self.raiz = self.construir_arbol(frecuencias)
        self.generar_codigos()
        texto_codificado = ''.join(self.codigos[c] for c in texto)
        longitud_original = len(texto) * 8
        longitud_comprimida = len(texto_codificado)
        ratio = longitud_comprimida / longitud_original if longitud_original > 0 else 0
        ahorro = (1 - ratio) * 100
        estadisticas = {
            'longitud_original_bits': longitud_original,
            'longitud_comprimida_bits': longitud_comprimida,
            'ratio_compresion': ratio,
            'ahorro_porcentual': ahorro,
            'caracteres_unicos': len(frecuencias)
        }
        return texto_codificado, self.codigos, estadisticas
    
    def decodificar_texto(self, texto_binario, codigos):
        if not texto_binario or not codigos:
            return ""
        codigos_inv = {v: k for k, v in codigos.items()}
        texto_decodificado = []
        codigo_actual = ""
        for bit in texto_binario:
            codigo_actual += bit
            if codigo_actual in codigos_inv:
                texto_decodificado.append(codigos_inv[codigo_actual])
                codigo_actual = ""
        return ''.join(texto_decodificado)
    
    def serializar_tabla(self, codigos):
        return json.dumps(codigos)
    
    def deserializar_tabla(self, tabla_json):
        return json.loads(tabla_json)


class LSBDetector:
  
    def __init__(self):
        self.image = None
        self.results = {}
        self.huffman = CodificadorHuffman()

    def load_image(self, image_path):
        try:
            self.image = cv2.imread(image_path)
            if self.image is None:
                raise ValueError("No se pudo cargar la imagen")
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            return True
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return False

    def _lsb_bits_brute(self, channel_2d):
        
        h, w = channel_2d.shape
        bits = []
        for i in range(h):
            for j in range(w):
                bits.append(str(channel_2d[i, j] & 1))
        return bits

    def _lsb_bits_divide_and_conquer(self, channel_2d, base_threshold=1024):
    
        h, w = channel_2d.shape
        n = h * w
        
        if n <= base_threshold:
            bits = []
            for i in range(h):
                for j in range(w):
                    bits.append(str(channel_2d[i, j] & 1))
            return bits
        
        mid = h // 2
      
        top_half = self._lsb_bits_divide_and_conquer(channel_2d[:mid, :], base_threshold)
        bottom_half = self._lsb_bits_divide_and_conquer(channel_2d[mid:, :], base_threshold)
     
        return top_half + bottom_half

    def _bits_to_text(self, lsb_bits):
        
        mensaje = ""
        for i in range(0, len(lsb_bits), 8):
            byte = lsb_bits[i:i+8]
            if len(byte) < 8:
                continue
            code = int(''.join(byte), 2)
            if 32 <= code <= 126:
                mensaje += chr(code)
            else:
                break
            if mensaje.endswith("END"):
                return mensaje[:-3]
        return mensaje if mensaje else None

    def extraer_mensaje_lsb(self, image_path, metodo='fuerza_bruta'):
        try:
            if not self.load_image(image_path):
                return None
            canal_rojo = self.image[:, :, 0]
            start = time.time()
            if metodo == 'divide_y_venceras':
                lsb_bits = self._lsb_bits_divide_and_conquer(canal_rojo)
                metodo_nombre = "Divide y Vencerás"
            else:
                lsb_bits = self._lsb_bits_brute(canal_rojo)
                metodo_nombre = "Fuerza Bruta"
            end = time.time()
            print(f"Tiempo {metodo_nombre}: {end - start:.5f} s")
            return self._bits_to_text(lsb_bits)
        except Exception as e:
            print(f"Error extrayendo mensaje: {e}")
            return None

    def ocultar_mensaje_huffman(self, image_path, mensaje, output_path, channel=0):
       
        try:
            if not self.load_image(image_path):
                return False
            print(f"\nOcultando mensaje con Huffman...")
            print(f"Mensaje original: '{mensaje}'")
            print(f"Longitud: {len(mensaje)} caracteres")
            
            texto_binario, tabla, stats = self.huffman.codificar_texto(mensaje)
            print(f"\nCompresión Huffman:")
            print(f"  - Cantidad de bits originales: {stats['longitud_original_bits']}")
            print(f"  - Bits comprimidos: {stats['longitud_comprimida_bits']}")
            print(f"  - Ahorro: {stats['ahorro_porcentual']:.1f}%")
            
            tabla_json = self.huffman.serializar_tabla(tabla)
            len_tabla = len(tabla_json)
            len_mensaje = len(texto_binario)
            cabecera = f"{len_tabla:08d}{tabla_json}{len_mensaje:08d}"
            
            mensaje_chars = ""
            for i in range(0, len(texto_binario), 8):
                byte = texto_binario[i:i+8]
                if len(byte) < 8:
                    byte = byte.ljust(8, '0')
                mensaje_chars += chr(int(byte, 2))
            
            payload_completo = cabecera + mensaje_chars + "END"
            bits_totales = ''.join(format(ord(c), '08b') for c in payload_completo)
            print(f"\nBits totales: {len(bits_totales)} bits ")
            
            canal = self.image[:, :, channel]
            capacidad = canal.size
            if len(bits_totales) > capacidad:
                print(f"Error: Mensaje muy grande ({len(bits_totales)} bits > {capacidad} píxeles)")
                return False
            
            img_stego = self.image.copy()
            bit_idx = 0
            for i in range(canal.shape[0]):
                for j in range(canal.shape[1]):
                    if bit_idx < len(bits_totales):
                        img_stego[i, j, channel] = (img_stego[i, j, channel] & 0xFE) | int(bits_totales[bit_idx])
                        bit_idx += 1
                    else:
                        break
            
            img_bgr = cv2.cvtColor(img_stego, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, img_bgr)
            print(f"Imagen guardada: {output_path}")
            print(f"Canal usado: {['Rojo', 'Verde', 'Azul'][channel]}")
            return True
        except Exception as e:
            print(f"Error ocultando mensaje: {e}")
            import traceback
            traceback.print_exc()
            return False

    def extraer_mensaje_huffman(self, image_path, metodo='fuerza_bruta', channel=0):
        try:
            if not self.load_image(image_path):
                return None, None
            canal = self.image[:, :, channel]
            print(f"Extrayendo bits (canal {channel}) con {metodo}...")
            
            inicio = time.time()
            if metodo == 'divide_y_venceras':
                bits_lsb = self._lsb_bits_divide_and_conquer(canal)
            else:
                bits_lsb = self._lsb_bits_brute(canal)
            tiempo = time.time() - inicio
            print(f"Tiempo: {tiempo:.5f} s")
            
            mensaje_raw = ""
            for i in range(0, len(bits_lsb), 8):
                byte = bits_lsb[i:i+8]
                if len(byte) < 8:
                    break
                mensaje_raw += chr(int(''.join(byte), 2))
                if mensaje_raw.endswith("END"):
                    mensaje_raw = mensaje_raw[:-3]
                    break
            
            if len(mensaje_raw) < 16:
                print("Datos insuficientes")
                return None, None
            
            try:
                len_tabla = int(mensaje_raw[:8])
                tabla_json = mensaje_raw[8:8+len_tabla]
                len_msg = int(mensaje_raw[8+len_tabla:16+len_tabla])
            except (ValueError, IndexError):
                print("Formato inválido")
                return None, None
            
            try:
                tabla = json.loads(tabla_json)
            except json.JSONDecodeError:
                print("Tabla JSON corrupta")
                return None, None
            
            inicio_datos = 16 + len_tabla
            bits_huffman = ''.join(format(ord(c), '08b') for c in mensaje_raw[inicio_datos:])
            bits_huffman = bits_huffman[:len_msg]
            mensaje = self.huffman.decodificar_texto(bits_huffman, tabla)
            
            if mensaje:
                print(f"Mensaje Huffman recuperado correctamente")
                print(f"Caracteres únicos en tabla: {len(tabla)}")
            return mensaje, tabla
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def chi_square_test(self, channel_data_flat):
        pairs_observed = []
        pairs_expected = []
        for i in range(0, 256, 2):
            if i + 1 < 256:
                even_count = np.sum(channel_data_flat == i)
                odd_count = np.sum(channel_data_flat == i + 1)
                pairs_observed.extend([even_count, odd_count])
                expected = (even_count + odd_count) / 2
                pairs_expected.extend([expected, expected])
        pairs_observed = np.array(pairs_observed)
        pairs_expected = np.array(pairs_expected)
        mask = pairs_expected > 0
        chi2 = np.sum((pairs_observed[mask] - pairs_expected[mask])**2 / pairs_expected[mask])
        df = len(pairs_observed[mask]) - 1
        p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 1
        return chi2, p_value, df

    def lsb_analysis(self, channel_flat):
        lsb_bits = channel_flat & 1
        lsb_stats = {
            'mean': np.mean(lsb_bits),
            'variance': np.var(lsb_bits),
            'entropy': self.calculate_entropy(lsb_bits),
            'runs_test': self.runs_test(lsb_bits),
            'expected_mean': 0.5,
            'expected_variance': 0.25
        }
        return lsb_stats

    def calculate_entropy(self, data):
        unique, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        return entropy

    def runs_test(self, binary_sequence):
        n = len(binary_sequence)
        if n == 0:
            return 0, 1
        runs = 1
        for i in range(1, n):
            if binary_sequence[i] != binary_sequence[i-1]:
                runs += 1
        ones = np.sum(binary_sequence)
        zeros = n - ones
        if ones == 0 or zeros == 0:
            return runs, 1
        expected_runs = (2 * ones * zeros) / n + 1
        variance_runs = (2 * ones * zeros * (2 * ones * zeros - n)) / (n**2 * (n - 1))
        if variance_runs <= 0:
            return runs, 1
        z_score = (runs - expected_runs) / np.sqrt(variance_runs)
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
        return z_score, p_value

    def spatial_correlation_analysis(self, channel_2d):
        h, w = channel_2d.shape
        horizontal_corr = np.corrcoef(channel_2d[:, :-1].flatten(), channel_2d[:, 1:].flatten())[0, 1] if w > 1 else 0
        vertical_corr = np.corrcoef(channel_2d[:-1, :].flatten(), channel_2d[1:, :].flatten())[0, 1] if h > 1 else 0
        return horizontal_corr, vertical_corr

    def calculate_suspicion_score(self, chi2_p_value, lsb_stats, h_corr, v_corr):

        weights = {'chi_square': 0.4, 'mean_deviation': 0.2, 'entropy': 0.2, 'correlation': 0.2}
        score = 0
        if chi2_p_value < 0.01:
            score += weights['chi_square']
        mean_deviation = abs(lsb_stats['mean'] - 0.5)
        if mean_deviation > 0.1:
            score += weights['mean_deviation']
        if lsb_stats['entropy'] > 0.99:
            score += weights['entropy']
        avg_correlation = (abs(h_corr) + abs(v_corr)) / 2
        if avg_correlation < 0.8:
            score += weights['correlation']
        return min(score, 1.0)

    def analizar_imagen_completo(self, image_path):
        print(f"\nANÁLISIS COMPLETO DE: {os.path.basename(image_path)}")
        print("="*60)
        
        if not self.load_image(image_path):
            return
        print(f"Imagen cargada: {self.image.shape}")
        
        print("\n--------- EXTRACCIÓN ESTÁNDAR -----------")
        print("\nMétodo Fuerza Bruta:")
        mensaje_fb = self.extraer_mensaje_lsb(image_path, 'fuerza_bruta')
        print("\nMétodo Divide y Vencerás:")
        mensaje_dyv = self.extraer_mensaje_lsb(image_path, 'divide_y_venceras')
        
        mensaje_estandar = mensaje_fb or mensaje_dyv
        if mensaje_estandar:
            print(f"\nMENSAJE ESTÁNDAR ENCONTRADO: '{mensaje_estandar}'")
        else:
            print("\nNo se encontró mensaje estándar")
        
        print("\n------------ EXTRACCIÓN HUFFMAN ----------")
        print("\nMétodo Fuerza Bruta:")
        mensaje_huff_fb, tabla_fb = self.extraer_mensaje_huffman(image_path, 'fuerza_bruta', 0)
        print("\nMétodo Divide y Vencerás:")
        mensaje_huff_dyv, tabla_dyv = self.extraer_mensaje_huffman(image_path, 'divide_y_venceras', 0)
        
        mensaje_huffman = mensaje_huff_fb or mensaje_huff_dyv
        if mensaje_huffman:
            print(f"\nMENSAJE HUFFMAN ENCONTRADO: '{mensaje_huffman}'")
        else:
            print("\nNo se encontró mensaje Huffman")
        
        print("\n---- ANÁLISIS ESTADÍSTICO (Canal Rojo) ----")
        channel = self.image[:, :, 0]
        flat = channel.flatten()
        chi2, pchi, df = self.chi_square_test(flat)
        lsb_stats = self.lsb_analysis(flat)
        hc, vc = self.spatial_correlation_analysis(channel)
        suspicion = self.calculate_suspicion_score(pchi, lsb_stats, hc, vc)
        
        print(f"Chi cuadrado: {chi2:.3f}, p-valor={pchi:.5f}, df={df}")
        print(f"LSB: mean={lsb_stats['mean']:.3f}, var={lsb_stats['variance']:.3f}, entropía={lsb_stats['entropy']:.3f}")
        print(f"Correlación espacial: horizontal={hc:.3f}, vertical={vc:.3f}")
        print(f"Puntuación de sospecha: {suspicion:.2f}/1.0")
        
        if mensaje_estandar or mensaje_huffman:
            print("\nEstado: ESTEGANOGRAFÍA DETECTADA")
        elif suspicion > 0.4:
            print("\nEstado: SOSPECHOSO - Posible esteganografía")
        else:
            print("\nEstado: NORMAL - No se detectó esteganografía")


class EsteganografiaLSB:
    
    @staticmethod
    def crear_imagen_con_mensaje(mensaje, nombre_archivo="imagen_con_mensaje.png"):
        try:
            width, height = 200, 200
            imagen = np.random.randint(50, 200, (height, width, 3), dtype=np.uint8)
            
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            
            if len(mensaje_binario) > width * height:
                print("Mensaje demasiado largo")
                return False
            
            bit_index = 0
            for i in range(height):
                for j in range(width):
                    if bit_index < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[bit_index])
                        bit_index += 1
                    else:
                        break
            
            Image.fromarray(imagen).save(nombre_archivo)
            print(f"Imagen creada: {nombre_archivo}")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def ocultar_mensaje_en_imagen_existente(mensaje, imagen_entrada, imagen_salida="imagen_estego.png"):
       
        try:
            imagen = cv2.imread(imagen_entrada)
            if imagen is None:
                print("No se pudo cargar la imagen")
                return False
            
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            height, width, _ = imagen.shape
            
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            
            if len(mensaje_binario) > width * height:
                print("Mensaje demasiado largo")
                return False
            
            bit_index = 0
            for i in range(height):
                for j in range(width):
                    if bit_index < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[bit_index])
                        bit_index += 1
                    else:
                        break
            
            Image.fromarray(imagen).save(imagen_salida)
            print(f"Mensaje oculto en: {imagen_salida}")
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False


def mostrar_menu():
    print("\n" + "="*60)
    print(" DETECTOR LSB ")
    print("="*60)
    print("1. Analizar imagen (FB + DyV + Huffman)")
    print("2. Crear imagen con mensaje estándar")
    print("3. Ocultar mensaje estándar en imagen existente")
    print("4. Ocultar mensaje con Huffman en imagen existente")
    print("5. Salir")
    print("="*60)


def seleccionar_imagen():
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    imagenes = []
    
    for ext in extensiones:
        imagenes.extend(glob.glob(ext))
    
    imagenes = list(dict.fromkeys(imagenes))
    
    if not imagenes:
        print("No se encontraron imágenes en el directorio actual")
        return None
    
    print("\nImágenes encontradas:")
    for i, img in enumerate(imagenes, 1):
        print(f" {i}. {img}")
    
    try:
        opcion = int(input(f"\nSelecciona una imagen (1-{len(imagenes)}): "))
        if 1 <= opcion <= len(imagenes):
            return imagenes[opcion - 1]
        else:
            print("Opción no válida")
            return None
    except ValueError:
        print("Entrada no válida")
        return None


def main():
    detector = LSBDetector()
    estego = EsteganografiaLSB()
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-5): ")
        
        if opcion == '1':
            imagen_path = seleccionar_imagen()
            if imagen_path:
                detector.analizar_imagen_completo(imagen_path)
        
        elif opcion == '2':
            mensaje = input("Ingresa el mensaje a ocultar: ")
            nombre_archivo = input("Nombre del archivo de salida (default: img_con_mensaje.png): ") or "img_con_mensaje.png"
            estego.crear_imagen_con_mensaje(mensaje, nombre_archivo)
        
        elif opcion == '3':
            mensaje = input("Ingresa el mensaje a ocultar: ")
            imagen_entrada = seleccionar_imagen()
            if imagen_entrada:
                imagen_salida = input("Nombre del archivo de salida (default: img_mensaje.png): ") or "img_mensaje.png"
                estego.ocultar_mensaje_en_imagen_existente(mensaje, imagen_entrada, imagen_salida)
        
        elif opcion == '4':
            mensaje = input("Ingresa el mensaje a ocultar: ")
            imagen_entrada = seleccionar_imagen()
            if imagen_entrada:
                imagen_salida = input("Nombre del archivo de salida (default: img_huffman.png): ") or "img_huffman.png"
                canal = input("Canal para ocultar (0=Rojo, 1=Verde, 2=Azul) [default=0]: ")
                canal = int(canal) if canal in ['0', '1', '2'] else 0
                detector.ocultar_mensaje_huffman(imagen_entrada, mensaje, imagen_salida, canal)
        
        elif opcion == '5':
            print("\nGracias por usar el programa :)\n")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    print("\n" + "="*60)
    print(" DETECTOR DE ESTEGANOGRAFÍA LSB")
    print("="*60)
    main()