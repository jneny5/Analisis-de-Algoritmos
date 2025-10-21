import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import os
import glob
import time

# ===============================================================
# CLASE DEL DETECTOR
# ===============================================================
class LSBDetector:
    def __init__(self):
        self.imagen = None
        self.resultados = {}

    def cargar_imagen(self, ruta_imagen):
        """Cargar imagen para análisis (RGB)"""
        try:
            self.imagen = cv2.imread(ruta_imagen)
            if self.imagen is None:
                raise ValueError("No se pudo cargar la imagen")
            self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB)
            return True
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return False

    # ---------------------------------------------------------------
    # FUERZA BRUTA
    # ---------------------------------------------------------------
    def extraer_bits_fuerza_bruta(self, canal_2d):
        """Extrae LSB recorriendo pixel por pixel (fuerza bruta)."""
        h, w = canal_2d.shape
        bits = []
        for i in range(h):
            for j in range(w):
                bits.append(str(canal_2d[i, j] & 1))
        return bits

    # ---------------------------------------------------------------
    # DIVIDE Y VENCERÁS
    # ---------------------------------------------------------------
    def extraer_bits_divide_y_venceras(self, canal_2d, umbral_base=1024):
        """
        Extrae LSB dividiendo recursivamente la matriz en 4 bloques
        hasta llegar a bloques pequeños (caso base).
        """
        h, w = canal_2d.shape
        n = h * w
        if n == 0:
            return []
        if n <= umbral_base:
            return [str(px & 1) for fila in canal_2d for px in fila]
        
        mitad_h, mitad_w = h // 2, w // 2
        bloques = [
            canal_2d[:mitad_h, :mitad_w],
            canal_2d[:mitad_h, mitad_w:],
            canal_2d[mitad_h:, :mitad_w],
            canal_2d[mitad_h:, mitad_w:]
        ]
        salida = []
        for bloque in bloques:
            salida.extend(self.extraer_bits_divide_y_venceras(bloque, umbral_base))
        return salida

    # ---------------------------------------------------------------
    # DECODIFICACIÓN DE TEXTO
    # ---------------------------------------------------------------
    def convertir_bits_a_texto(self, bits_lsb):
        """Convierte una secuencia de bits (lista de '0'/'1') a texto hasta 'END'."""
        mensaje = ""
        for i in range(0, len(bits_lsb), 8):
            byte = bits_lsb[i:i+8]
            if len(byte) < 8:
                continue
            codigo = int(''.join(byte), 2)
            if 32 <= codigo <= 126:
                mensaje += chr(codigo)
            else:
                break
            if mensaje.endswith("END"):
                return mensaje[:-3]
        return mensaje if mensaje else None

    # ---------------------------------------------------------------
    # API PARA EXTRACCIÓN
    # ---------------------------------------------------------------
    def extraer_mensaje_lsb(self, ruta_imagen):
        """Extraer mensaje oculto usando LSB (FUERZA BRUTA) del canal rojo."""
        try:
            if not self.cargar_imagen(ruta_imagen):
                return None
            canal_rojo = self.imagen[:, :, 0]
            inicio = time.time()
            bits_lsb = self.extraer_bits_fuerza_bruta(canal_rojo)
            fin = time.time()
            print(f"Tiempo Fuerza Bruta: {fin - inicio:.5f} s")
            return self.convertir_bits_a_texto(bits_lsb)
        except Exception as e:
            print(f"Error extrayendo mensaje (FB): {e}")
            return None

    def extraer_mensaje_divide_y_venceras(self, ruta_imagen):
        """Extraer mensaje oculto usando LSB (DIVIDE Y VENCERÁS) del canal rojo."""
        try:
            if not self.cargar_imagen(ruta_imagen):
                return None
            canal_rojo = self.imagen[:, :, 0]
            inicio = time.time()
            bits_lsb = self.extraer_bits_divide_y_venceras(canal_rojo)
            fin = time.time()
            print(f"Tiempo Divide y Venceras: {fin - inicio:.5f} s")
            return self.convertir_bits_a_texto(bits_lsb)
        except Exception as e:
            print(f"Error extrayendo mensaje (DyV): {e}")
            return None

    # ---------------------------------------------------------------
    # PRUEBAS ESTADÍSTICAS
    # ---------------------------------------------------------------
    def prueba_chi_cuadrado(self, datos_canal_plano):
        pares_observados = []
        pares_esperados = []
        for i in range(0, 256, 2):
            if i + 1 < 256:
                conteo_par = np.sum(datos_canal_plano == i)
                conteo_impar = np.sum(datos_canal_plano == i + 1)
                pares_observados.extend([conteo_par, conteo_impar])
                esperado = (conteo_par + conteo_impar) / 2
                pares_esperados.extend([esperado, esperado])
        pares_observados = np.array(pares_observados)
        pares_esperados = np.array(pares_esperados)
        mascara = pares_esperados > 0
        chi2 = np.sum((pares_observados[mascara] - pares_esperados[mascara])**2 / pares_esperados[mascara])
        grados_libertad = len(pares_observados[mascara]) - 1
        valor_p = 1 - stats.chi2.cdf(chi2, grados_libertad) if grados_libertad > 0 else 1
        return chi2, valor_p, grados_libertad

    def analisis_lsb(self, canal_plano):
        bits_lsb = canal_plano & 1
        estadisticas_lsb = {
            'media': np.mean(bits_lsb),
            'varianza': np.var(bits_lsb),
            'entropia': self.calcular_entropia(bits_lsb),
            'prueba_rachas': self.prueba_rachas(bits_lsb),
            'media_esperada': 0.5,
            'varianza_esperada': 0.25
        }
        return estadisticas_lsb

    def calcular_entropia(self, datos):
        unicos, conteos = np.unique(datos, return_counts=True)
        probabilidades = conteos / len(datos)
        entropia = -np.sum(probabilidades * np.log2(probabilidades + 1e-10))
        return entropia

    def prueba_rachas(self, secuencia_binaria):
        n = len(secuencia_binaria)
        if n == 0:
            return 0, 1
        rachas = 1
        for i in range(1, n):
            if secuencia_binaria[i] != secuencia_binaria[i-1]:
                rachas += 1
        unos = np.sum(secuencia_binaria)
        ceros = n - unos
        if unos == 0 or ceros == 0:
            return rachas, 1
        rachas_esperadas = (2 * unos * ceros) / n + 1
        varianza_rachas = (2 * unos * ceros * (2 * unos * ceros - n)) / (n**2 * (n - 1))
        if varianza_rachas <= 0:
            return rachas, 1
        puntuacion_z = (rachas - rachas_esperadas) / np.sqrt(varianza_rachas)
        valor_p = 2 * (1 - stats.norm.cdf(abs(puntuacion_z)))
        return puntuacion_z, valor_p

    def analisis_correlacion_espacial(self, canal_2d):
        h, w = canal_2d.shape
        correlacion_horizontal = np.corrcoef(canal_2d[:, :-1].flatten(), canal_2d[:, 1:].flatten())[0, 1] if w > 1 else 0
        correlacion_vertical = np.corrcoef(canal_2d[:-1, :].flatten(), canal_2d[1:, :].flatten())[0, 1] if h > 1 else 0
        return correlacion_horizontal, correlacion_vertical

    def calcular_puntuacion_sospecha(self, valor_p_chi2, estadisticas_lsb, correlacion_h, correlacion_v):
        pesos = {'chi_cuadrado': 0.4, 'desviacion_media': 0.2, 'entropia': 0.2, 'correlacion': 0.2}
        puntuacion = 0
        if valor_p_chi2 < 0.01:
            puntuacion += pesos['chi_cuadrado']
        desviacion_media = abs(estadisticas_lsb['media'] - 0.5)
        if desviacion_media > 0.1:
            puntuacion += pesos['desviacion_media']
        if estadisticas_lsb['entropia'] > 0.99:
            puntuacion += pesos['entropia']
        correlacion_promedio = (abs(correlacion_h) + abs(correlacion_v)) / 2
        if correlacion_promedio < 0.8:
            puntuacion += pesos['correlacion']
        return min(puntuacion, 1.0)

    # ---------------------------------------------------------------
    def analizar_imagen_completo(self, ruta_imagen):
        """Análisis + comparativa FB vs DyV en la imagen original."""
        print(f"\nANALISIS COMPLETO DE: {os.path.basename(ruta_imagen)}")
        print("="*60)
        if not self.cargar_imagen(ruta_imagen):
            return
        print(f"Imagen cargada: {self.imagen.shape}")

        print("\nEXTRACCION DE MENSAJE (Fuerza Bruta):")
        mensaje_fb = self.extraer_mensaje_lsb(ruta_imagen)
        print("EXTRACCION DE MENSAJE (Divide y Venceras):")
        mensaje_dyv = self.extraer_mensaje_divide_y_venceras(ruta_imagen)

        mensaje = mensaje_fb or mensaje_dyv
        if mensaje:
            print(f"MENSAJE ENCONTRADO: '{mensaje}'")
        else:
            print("No se encontro mensaje legible")

        print("\nANALISIS ESTADISTICO (Canal Rojo):")
        canal = self.imagen[:, :, 0]
        plano = canal.flatten()
        chi2, valor_p_chi, grados_libertad = self.prueba_chi_cuadrado(plano)
        estadisticas_lsb = self.analisis_lsb(plano)
        correlacion_h, correlacion_v = self.analisis_correlacion_espacial(canal)
        sospecha = self.calcular_puntuacion_sospecha(valor_p_chi, estadisticas_lsb, correlacion_h, correlacion_v)

        print(f"Chi2 df={grados_libertad}  p={valor_p_chi:.4g}")
        print(f"LSB media={estadisticas_lsb['media']:.3f} var={estadisticas_lsb['varianza']:.3f} entropia={estadisticas_lsb['entropia']:.3f}")
        print(f"Correlacion H={correlacion_h:.3f}  V={correlacion_v:.3f}")
        print(f"Puntuacion de sospecha: {sospecha:.2f}/1.0")
        if mensaje:
            print("Estado: ESTEGANOGRAFIA DETECTADA")
        elif sospecha > 0.4:
            print("Estado: SOSPECHOSO - Posible esteganografia")
        else:
            print("Estado: NORMAL - No se detecto esteganografia")

    # ---------------------------------------------------------------
    # BENCHMARK N vs TIEMPO
    # ---------------------------------------------------------------
    def benchmark_n_vs_tiempo(self, ruta_imagen, 
                             tamaños=(64, 128, 256, 512, 768, 1024, 1536, 2048), 
                             umbral_base=1024, 
                             repeticiones=3,
                             directorio_guardar='graficas_benchmark'):
        """
        Benchmark completo con múltiples gráficos de análisis.
        Mide tiempos con múltiples repeticiones para mayor precisión.
        """
        if not self.cargar_imagen(ruta_imagen):
            print("No se pudo cargar la imagen para benchmark.")
            return

        if not os.path.exists(directorio_guardar):
            os.makedirs(directorio_guardar)

        original = self.imagen[:, :, 0]
        
        ns = []
        tiempos_fb_promedio = []
        tiempos_dyv_promedio = []
        tiempos_fb_desv = []
        tiempos_dyv_desv = []
        
        print("\n" + "="*70)
        print("BENCHMARK: n vs tiempo (Fuerza Bruta vs Divide y Venceras)")
        print("="*70)
        print(f"Repeticiones por tamaño: {repeticiones}")
        print(f"Tamaños a probar: {tamaños}")
        print("-"*70)

        for tamaño in tamaños:
            print(f"\nProbando tamaño {tamaño}x{tamaño} = {tamaño*tamaño:,} pixeles...")
            
            redimensionada = cv2.resize(original, (tamaño, tamaño), interpolation=cv2.INTER_NEAREST)
            
            tiempos_fb_temp = []
            tiempos_dyv_temp = []
            
            for rep in range(repeticiones):
                t0 = time.time()
                _ = self.extraer_bits_fuerza_bruta(redimensionada)
                t1 = time.time()
                tiempo_fb = t1 - t0
                tiempos_fb_temp.append(tiempo_fb)
                
                t2 = time.time()
                _ = self.extraer_bits_divide_y_venceras(redimensionada, umbral_base=umbral_base)
                t3 = time.time()
                tiempo_dyv = t3 - t2
                tiempos_dyv_temp.append(tiempo_dyv)
                
                print(f"  Rep {rep+1}/{repeticiones}: FB={tiempo_fb:.5f}s | DyV={tiempo_dyv:.5f}s")
            
            fb_promedio = np.mean(tiempos_fb_temp)
            dyv_promedio = np.mean(tiempos_dyv_temp)
            fb_desv = np.std(tiempos_fb_temp)
            dyv_desv = np.std(tiempos_dyv_temp)
            
            ns.append(tamaño * tamaño)
            tiempos_fb_promedio.append(fb_promedio)
            tiempos_dyv_promedio.append(dyv_promedio)
            tiempos_fb_desv.append(fb_desv)
            tiempos_dyv_desv.append(dyv_desv)
            
            aceleracion = fb_promedio / dyv_promedio if dyv_promedio > 0 else 0
            mejora_porcentual = ((fb_promedio - dyv_promedio) / fb_promedio * 100) if fb_promedio > 0 else 0
            
            print(f"  Promedio FB: {fb_promedio:.5f}s (desv: {fb_desv:.5f}s)")
            print(f"  Promedio DyV: {dyv_promedio:.5f}s (desv: {dyv_desv:.5f}s)")
            print(f"  Aceleracion: {aceleracion:.2f}x | Mejora: {mejora_porcentual:.1f}%")

        ns = np.array(ns)
        tiempos_fb_promedio = np.array(tiempos_fb_promedio)
        tiempos_dyv_promedio = np.array(tiempos_dyv_promedio)
        tiempos_fb_desv = np.array(tiempos_fb_desv)
        tiempos_dyv_desv = np.array(tiempos_dyv_desv)
        
        # Crear graficos
        plt.figure(figsize=(14, 10))
        
        # Grafico 1: Comparacion de tiempos (escala lineal)
        plt.subplot(2, 2, 1)
        plt.errorbar(ns, tiempos_fb_promedio, yerr=tiempos_fb_desv, 
                    fmt='r-o', linewidth=2, markersize=8, capsize=5, 
                    label='Fuerza Bruta O(n)', alpha=0.8)
        plt.errorbar(ns, tiempos_dyv_promedio, yerr=tiempos_dyv_desv, 
                    fmt='g-s', linewidth=2, markersize=8, capsize=5, 
                    label='Divide y Venceras O(n)', alpha=0.8)
        plt.xlabel('n (numero de pixeles)', fontsize=12, fontweight='bold')
        plt.ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
        plt.title('Comparacion Temporal: Fuerza Bruta vs Divide y Venceras\n(Escala Lineal)', 
                 fontsize=13, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Grafico 2: Comparacion de tiempos (escala logaritmica)
        plt.subplot(2, 2, 2)
        plt.loglog(ns, tiempos_fb_promedio, 'r-o', linewidth=2, markersize=8, 
                  label='Fuerza Bruta', alpha=0.8)
        plt.loglog(ns, tiempos_dyv_promedio, 'g-s', linewidth=2, markersize=8, 
                  label='Divide y Venceras', alpha=0.8)
        
        referencia_lineal = ns / ns[0] * tiempos_fb_promedio[0]
        plt.loglog(ns, referencia_lineal, 'k--', linewidth=1.5, alpha=0.5, label='O(n) teorico')
        
        plt.xlabel('n (numero de pixeles)', fontsize=12, fontweight='bold')
        plt.ylabel('Tiempo (segundos)', fontsize=12, fontweight='bold')
        plt.title('Comparacion Temporal\n(Escala Log-Log)', fontsize=13, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, which='both', linestyle='--')
        
        # Grafico 3: Aceleracion
        plt.subplot(2, 2, 3)
        aceleraciones = tiempos_fb_promedio / tiempos_dyv_promedio
        plt.plot(ns, aceleraciones, 'b-o', linewidth=2.5, markersize=10, alpha=0.8)
        plt.axhline(y=1, color='r', linestyle='--', linewidth=2, alpha=0.7, label='Sin mejora (1x)')
        plt.fill_between(ns, 1, aceleraciones, where=(aceleraciones >= 1), alpha=0.3, color='green', 
                        label='Zona de mejora')
        plt.xlabel('n (numero de pixeles)', fontsize=12, fontweight='bold')
        plt.ylabel('Aceleracion (FB/DyV)', fontsize=12, fontweight='bold')
        plt.title('Factor de Aceleracion\n(Cuanto mas rapido es DyV)', 
                 fontsize=13, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Grafico 4: Mejora porcentual
        plt.subplot(2, 2, 4)
        mejora_porcentual = ((tiempos_fb_promedio - tiempos_dyv_promedio) / tiempos_fb_promedio) * 100
        colores = ['green' if m > 0 else 'red' for m in mejora_porcentual]
        plt.bar(range(len(tamaños)), mejora_porcentual, color=colores, alpha=0.7, edgecolor='black')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
        plt.xticks(range(len(tamaños)), [f"{t}x{t}" for t in tamaños], rotation=45)
        plt.xlabel('Tamaño de imagen', fontsize=12, fontweight='bold')
        plt.ylabel('Mejora (%)', fontsize=12, fontweight='bold')
        plt.title('Mejora Porcentual de Divide y Venceras\n(valores positivos = mejor)', 
                 fontsize=13, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        ruta_grafica_principal = os.path.join(directorio_guardar, 'comparativa_completa.png')
        plt.savefig(ruta_grafica_principal, dpi=150, bbox_inches='tight')
        print(f"\nGrafica principal guardada: {os.path.abspath(ruta_grafica_principal)}")
        
        # Grafico adicional: Analisis de Complejidad
        plt.figure(figsize=(12, 6))
        
        def modelo_lineal(n, a, b):
            return a * n + b
        
        plt.subplot(1, 2, 1)
        parametros_fb, _ = curve_fit(modelo_lineal, ns, tiempos_fb_promedio)
        ajuste_fb = modelo_lineal(ns, *parametros_fb)
        
        plt.plot(ns, tiempos_fb_promedio, 'ro', markersize=10, label='Datos FB', alpha=0.7)
        plt.plot(ns, ajuste_fb, 'r--', linewidth=2, label=f'Ajuste FB: {parametros_fb[0]:.2e}*n + {parametros_fb[1]:.4f}')
        plt.xlabel('n (pixeles)', fontsize=12, fontweight='bold')
        plt.ylabel('Tiempo (s)', fontsize=12, fontweight='bold')
        plt.title('Fuerza Bruta: Complejidad Temporal', fontsize=13, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        parametros_dyv, _ = curve_fit(modelo_lineal, ns, tiempos_dyv_promedio)
        ajuste_dyv = modelo_lineal(ns, *parametros_dyv)
        
        plt.plot(ns, tiempos_dyv_promedio, 'go', markersize=10, label='Datos DyV', alpha=0.7)
        plt.plot(ns, ajuste_dyv, 'g--', linewidth=2, label=f'Ajuste DyV: {parametros_dyv[0]:.2e}*n + {parametros_dyv[1]:.4f}')
        plt.xlabel('n (pixeles)', fontsize=12, fontweight='bold')
        plt.ylabel('Tiempo (s)', fontsize=12, fontweight='bold')
        plt.title('Divide y Venceras: Complejidad Temporal', fontsize=13, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        ruta_grafica_complejidad = os.path.join(directorio_guardar, 'analisis_complejidad.png')
        plt.savefig(ruta_grafica_complejidad, dpi=150, bbox_inches='tight')
        print(f"Analisis de complejidad guardado: {os.path.abspath(ruta_grafica_complejidad)}")
        
        # Resumen estadistico
        print("\n" + "="*70)
        print("RESUMEN ESTADISTICO DEL BENCHMARK")
        print("="*70)
        print(f"\nTamaños probados: {len(tamaños)}")
        print(f"Rango de n: {ns[0]:,} a {ns[-1]:,} pixeles")
        print(f"\nFUERZA BRUTA:")
        print(f"   Tiempo minimo: {np.min(tiempos_fb_promedio):.5f}s (n={ns[np.argmin(tiempos_fb_promedio)]:,})")
        print(f"   Tiempo maximo: {np.max(tiempos_fb_promedio):.5f}s (n={ns[np.argmax(tiempos_fb_promedio)]:,})")
        print(f"   Tiempo promedio: {np.mean(tiempos_fb_promedio):.5f}s")
        print(f"   Coeficiente lineal: {parametros_fb[0]:.2e}")
        
        print(f"\nDIVIDE Y VENCERAS:")
        print(f"   Tiempo minimo: {np.min(tiempos_dyv_promedio):.5f}s (n={ns[np.argmin(tiempos_dyv_promedio)]:,})")
        print(f"   Tiempo maximo: {np.max(tiempos_dyv_promedio):.5f}s (n={ns[np.argmax(tiempos_dyv_promedio)]:,})")
        print(f"   Tiempo promedio: {np.mean(tiempos_dyv_promedio):.5f}s")
        print(f"   Coeficiente lineal: {parametros_dyv[0]:.2e}")
        
        print(f"\nCOMPARACION:")
        print(f"   Aceleracion promedio: {np.mean(aceleraciones):.2f}x")
        print(f"   Aceleracion maxima: {np.max(aceleraciones):.2f}x (n={ns[np.argmax(aceleraciones)]:,})")
        print(f"   Mejora porcentual promedio: {np.mean(mejora_porcentual):.1f}%")
        print(f"   Ratio de eficiencia (DyV/FB): {parametros_dyv[0]/parametros_fb[0]:.2f}")
        
        print("\nBenchmark completado exitosamente")
        print("="*70)
        
        plt.show()

# ===============================================================
# CLASE ESTEGANOGRAFÍA
# ===============================================================
class EsteganografiaLSB:
    @staticmethod
    def crear_imagen_con_mensaje(mensaje, nombre_archivo="imagen_con_mensaje.png"):
        try:
            ancho, alto = 200, 200
            imagen = np.random.randint(50, 200, (alto, ancho, 3), dtype=np.uint8)
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            if len(mensaje_binario) > ancho * alto:
                print("Mensaje demasiado largo")
                return False
            indice_bit = 0
            for i in range(alto):
                for j in range(ancho):
                    if indice_bit < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[indice_bit])
                        indice_bit += 1
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
            alto, ancho, _ = imagen.shape
            mensaje_con_fin = mensaje + "END"
            mensaje_binario = ''.join(format(ord(c), '08b') for c in mensaje_con_fin)
            if len(mensaje_binario) > ancho * alto:
                print("Mensaje demasiado largo")
                return False
            indice_bit = 0
            for i in range(alto):
                for j in range(ancho):
                    if indice_bit < len(mensaje_binario):
                        imagen[i, j, 0] = (imagen[i, j, 0] & 0xFE) | int(mensaje_binario[indice_bit])
                        indice_bit += 1
                    else:
                        break
            Image.fromarray(imagen).save(imagen_salida)
            print(f"Mensaje oculto en: {imagen_salida}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

# ===============================================================
# FUNCIONES AUXILIARES
# ===============================================================
def mostrar_menu():
    print("\n============================================================")
    print(" DETECTOR DE MSJS OCULTOS (LSB) - Divide y Vencerás")
    print("============================================================")
    print("1. Analizar imagen (FB + DyV + estadisticas)")
    print("2. Crear imagen con esteganografia (nueva)")
    print("3. Ocultar mensaje en imagen existente")
    print("4. Benchmark n vs tiempo (FB vs DyV)")
    print("5. Salir")
    print("============================================================")

def listar_imagenes():
    extensiones = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
    imagenes = []
    for ext in extensiones:
        imagenes.extend(glob.glob(ext))
    imagenes = list(dict.fromkeys([img for img in imagenes]))
    if not imagenes:
        print("No se encontraron imagenes en el directorio actual")
        return []
    print("\nImagenes encontradas:")
    for i, img in enumerate(imagenes, 1):
        print(f"  {i}. {img}")
    return imagenes

# ===============================================================
# BLOQUE PRINCIPAL
# ===============================================================
if __name__ == "__main__":
    detector = LSBDetector()
    estego = EsteganografiaLSB()
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opcion: ")
        
        if opcion == "1":
            imgs = listar_imagenes()
            if not imgs:
                continue
            idx = int(input("Selecciona una imagen (numero): ")) - 1
            if idx < 0 or idx >= len(imgs):
                print("Opcion invalida.")
                continue
            ruta_imagen = imgs[idx]
            detector.analizar_imagen_completo(ruta_imagen)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "2":
            mensaje = input("\nIngresa el mensaje que desea ocultar: ")
            nombre = input("Nombre del archivo (sin extension): ") or "imagen_con_mensaje"
            canal = int(input("Canal (0=R, 1=G, 2=B, default 0): ") or 0)
            estego.crear_imagen_con_mensaje(mensaje, f"{nombre}.png")
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "3":
            imgs = listar_imagenes()
            if not imgs:
                continue
            idx = int(input("Selecciona imagen base (numero): ")) - 1
            if idx < 0 or idx >= len(imgs):
                print("Opcion invalida.")
                continue
            mensaje = input("Mensaje a ocultar: ")
            nombre_salida = input("Archivo de salida (default: imagen_estego.png): ") or "imagen_estego.png"
            estego.ocultar_mensaje_en_imagen_existente(mensaje, imgs[idx], nombre_salida)
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "4":
            print("\n" + "="*60)
            print("BENCHMARK - ANALISIS DE COMPLEJIDAD TEMPORAL")
            print("="*60)
            
            imgs = listar_imagenes()
            if not imgs:
                continue
            idx = int(input("Selecciona imagen para pruebas (numero): ")) - 1
            if idx < 0 or idx >= len(imgs):
                print("Opcion invalida.")
                continue
            ruta_imagen = imgs[idx]
            
            print("\nConfiguracion del benchmark:")
            print("Puedes usar los valores por defecto o personalizarlos")
            print("-"*60)
            
            tamaños_str = input("\nTamaños (px) separados por coma\n   [Default: 64,128,256,512,768,1024,1536,2048]: ")
            if tamaños_str:
                try:
                    tamaños = tuple(int(x.strip()) for x in tamaños_str.split(',') if int(x.strip()) > 0)
                    if len(tamaños) == 0:
                        tamaños = (64, 128, 256, 512, 768, 1024, 1536, 2048)
                except:
                    print("Formato invalido, usando valores por defecto")
                    tamaños = (64, 128, 256, 512, 768, 1024, 1536, 2048)
            else:
                tamaños = (64, 128, 256, 512, 768, 1024, 1536, 2048)
            
            reps_str = input("\nNumero de repeticiones por tamaño\n   [Default: 3]: ")
            if reps_str:
                try:
                    repeticiones = int(reps_str)
                    if repeticiones < 1:
                        repeticiones = 3
                except:
                    print("Formato invalido, usando 3 repeticiones")
                    repeticiones = 3
            else:
                repeticiones = 3
            
            umbral_str = input("\nUmbral para Divide y Venceras\n   [Default: 1024]: ")
            if umbral_str:
                try:
                    umbral_base = int(umbral_str)
                    if umbral_base < 1:
                        umbral_base = 1024
                except:
                    print("Formato invalido, usando 1024")
                    umbral_base = 1024
            else:
                umbral_base = 1024
            
            directorio_salida = input("\nDirectorio para guardar graficas\n   [Default: graficas_benchmark]: ")
            if not directorio_salida:
                directorio_salida = 'graficas_benchmark'
            
            print("\nConfiguracion establecida:")
            print(f"   Tamaños: {tamaños}")
            print(f"   Repeticiones: {repeticiones}")
            print(f"   Umbral: {umbral_base}")
            print(f"   Directorio: {directorio_salida}")
            print("\nADVERTENCIA: Este proceso puede tardar varios minutos")
            print("   dependiendo de los tamaños seleccionados.")
            
            continuar = input("\nDeseas continuar? (s/n): ").lower()
            if continuar in ['s', 'si', 'yes', 'y']:
                print("\nIniciando benchmark...")
                detector.benchmark_n_vs_tiempo(
                    ruta_imagen, 
                    tamaños=tamaños,
                    umbral_base=umbral_base,
                    repeticiones=repeticiones,
                    directorio_guardar=directorio_salida
                )
            else:
                print("Benchmark cancelado")
            
            input("\nPresiona Enter para continuar...")
            
        elif opcion == "5":
            print("\n" + "="*60)
            print("Gracias por usar el Detector LSB")
            print("Programa finalizado exitosamente")
            print("="*60)
            break
            
        else:
            print("Opcion no valida.")