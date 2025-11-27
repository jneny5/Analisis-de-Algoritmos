# 🔐 Detector LSB con Compresión Huffman

**Equipo Snoopy** | Proyecto de Esteganografía LSB

---

## Descripción del Proyecto

La **esteganografía LSB (Least Significant Bit)** es una técnica ampliamente utilizada para ocultar información secreta dentro de imágenes digitales, modificando el bit menos significativo de los valores de píxeles. Aunque es efectiva, puede ser detectada mediante análisis estadístico avanzado.

Este proyecto proporciona una **herramienta completa** que no solo detecta esteganografía LSB en imágenes, sino que también implementa un **método mejorado de ocultamiento** que utiliza la **compresión Huffman** para optimizar el espacio del payload esteganográfico. Al comprimir los mensajes antes de ocultarlos, se reduce significativamente la cantidad de bits modificados, dificultando la detección y aumentando la capacidad de ocultamiento.

### Problema que Resuelve

- **Detección:** Identificar imágenes que contengan mensajes ocultos mediante técnicas LSB estándar o con compresión Huffman.
- **Análisis Forense:** Proporcionar métricas estadísticas que revelan patrones no naturales en los bits menos significativos.
- **Esteganografía Optimizada:** Permitir el ocultamiento de mensajes más largos en imágenes mediante compresión de datos.

---

## aracterísticas Principales

### Análisis y Detección
- **Extracción de mensajes LSB** mediante dos algoritmos:
- **Fuerza Bruta:** Iteración directa sobre todos los píxeles
- **Divide y Vencerás:** Algoritmo recursivo optimizado para grandes imágenes
- **Detección de mensajes comprimidos con Huffman:** Descompresión automática de payloads esteganográficos
- **Comparación de rendimiento** entre métodos de extracción

### 📊 Análisis Estadístico Avanzado
- **Test de Chi-Cuadrado (χ²):** Detecta desviaciones de la distribución uniforme esperada en los LSB
- **Análisis de Entropía:** Mide el nivel de aleatoriedad en los bits menos significativos
- **Runs Test:** Evalúa la secuencialidad y patrones en secuencias binarias
- **Correlación Espacial:** Analiza la correlación entre píxeles adyacentes (horizontal y vertical)
- **Puntuación de Sospecha:** Métrica combinada que indica la probabilidad de esteganografía

### Funcionalidades de Esteganografía
- **Creación de imágenes** con mensajes ocultos desde cero
- **Ocultamiento en imágenes existentes** con LSB estándar
- **Ocultamiento con compresión Huffman:**
  - Reducción del tamaño del mensaje hasta un 50-60%
  - Selección de canal de color (Rojo, Verde, Azul)
  - Inclusión de tabla de códigos Huffman en el payload

### Interfaz 
- **CLI (Command Line Interface):** Menú interactivo para usuarios avanzados
- **GUI (Graphical User Interface):** Interfaz moderna con `tkinter` para usuarios generales

---

##  Instalación

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/lsb-detector-huffman.git
cd lsb-detector-huffman
```

### Paso 2: Instalar Dependencias
```bash
pip install opencv-python numpy pillow scipy
```

**Dependencias incluidas en Python estándar:** `json`, `heapq`, `tkinter`

### Verificación de Instalación
```bash
python huffman.py
```

---

## 📖 Uso

### Interfaz Gráfica (GUI)

Para iniciar la aplicación con interfaz gráfica:

```bash
python gui.py
```

La GUI ofrece cuatro pestañas principales:

1. **Realizar Análisis:**
   - Selecciona una imagen
   - Ejecuta análisis completo (extracción estándar + Huffman + estadísticas)
   - Visualiza resultados en tiempo real

2. **Crear Imagen:**
   - Genera una nueva imagen (200x200 px) con mensaje oculto
   - Ideal para pruebas rápidas

3. **Ocultar Estándar:**
   - Oculta mensajes en imágenes existentes usando LSB estándar
   - Sin compresión

4. **Ocultar usando Huffman:**
   - Oculta mensajes con compresión Huffman
   - Selección de canal RGB
   - Mayor eficiencia de espacio

### Interfaz de Línea de Comandos (CLI)

Para iniciar el menú interactivo:

```bash
python huffman.py
```

**Opciones del menú:**

```
1. Analizar imagen (FB + DyV + Huffman)
   - Realiza análisis completo con ambos métodos de extracción
   - Muestra estadísticas detalladas y puntuación de sospecha

2. Crear imagen con mensaje estándar
   - Genera imagen nueva con mensaje LSB estándar

3. Ocultar mensaje estándar en imagen existente
   - Modifica imagen existente para incluir mensaje sin compresión

4. Ocultar mensaje con Huffman en imagen existente
   - Comprime y oculta mensaje con algoritmo Huffman
   - Permite seleccionar canal de color

5. Salir
```

---

## Arquitectura del Proyecto

### Archivos Principales

```
lsb-detector-huffman/
│
├── huffman.py          # Módulo principal con todas las clases
├── gui.py              # Interfaz gráfica 
└── README.md           # Documentación del proyecto
```

### Clases Clave

#### `CodificadorHuffman`
**Propósito:** Implementa la codificación y decodificación de Huffman para compresión de texto.

**Responsabilidades:**
- Calcular frecuencias de caracteres en el texto
- Construir árbol de Huffman usando una cola de prioridad (heap)
- Generar códigos binarios óptimos para cada carácter
- Codificar texto a secuencia binaria comprimida
- Decodificar secuencias binarias a texto original
- Serializar/deserializar tablas de códigos en formato JSON

**Métodos destacados:**
- `codificar_texto()`: Comprime texto y retorna estadísticas de ahorro
- `decodificar_texto()`: Recupera texto original desde secuencia binaria
- `construir_arbol()`: Genera árbol de Huffman óptimo

---

#### `LSBDetector`
**Propósito:** Motor principal de análisis y detección de esteganografía LSB.

**Responsabilidades:**
- Cargar y procesar imágenes (conversión RGB)
- Extraer mensajes LSB con dos algoritmos (Fuerza Bruta y Divide y Vencerás)
- Detectar y extraer mensajes con compresión Huffman
- Ejecutar análisis estadísticos avanzados
- Calcular puntuación de sospecha de esteganografía
- Ocultar mensajes con compresión Huffman en imágenes

**Métodos destacados:**
- `analizar_imagen_completo()`: Ejecuta batería completa de pruebas
- `extraer_mensaje_huffman()`: Recupera y descomprime mensajes Huffman
- `ocultar_mensaje_huffman()`: Comprime y oculta mensajes optimizados
- `chi_square_test()`: Aplica test estadístico χ² a pares de valores
- `spatial_correlation_analysis()`: Mide correlación entre píxeles adyacentes

---

#### `EsteganografiaLSB`
**Propósito:** Proporciona utilidades para crear y modificar imágenes con esteganografía LSB estándar.

**Responsabilidades:**
- Generar imágenes sintéticas con mensajes ocultos
- Modificar imágenes existentes para ocultar mensajes
- Implementar protocolo de terminación ("END") para extracción

**Métodos destacados:**
- `crear_imagen_con_mensaje()`: Genera imagen 200x200 con mensaje
- `ocultar_mensaje_en_imagen_existente()`: Modifica LSB del canal rojo

---

## Análisis Estadístico: Fundamentos

### ¿Por qué son importantes estas métricas?

#### Test de Chi-Cuadrado (χ^2)
El test de Chi-Cuadrado compara la distribución observada de valores de píxeles con la distribución esperada en una imagen natural. En imágenes sin esteganografía, los valores de píxeles adyacentes (pares e impares) deberían tener frecuencias similares.

**Interpretación:**
- **p-valor < 0.01:** Alta probabilidad de esteganografía (rechaza hipótesis nula)
- **p-valor > 0.05:** Imagen probablemente limpia
- **χ² elevado:** Indica desviación significativa de la aleatoriedad esperada

---

#### Entropía 
La entropía mide el grado de aleatoriedad o incertidumbre en los bits LSB. En imágenes naturales, los LSB tienen entropía moderada (~0.7-0.9). La esteganografía tiende a **aumentar** la entropía hacia el máximo teórico (1.0).

**Interpretación:**
- **Entropía ≈ 1.0:** Bits altamente aleatorios (sospechoso de esteganografía)
- **Entropía < 0.8:** Distribución natural de bits
- **Fórmula:** H = -Σ p(x) log₂ p(x)

---

#### Correlación Espacial
Las imágenes naturales presentan alta correlación entre píxeles vecinos (típicamente > 0.9) debido a la continuidad visual. La esteganografía LSB **reduce** esta correlación al introducir cambios pseudo-aleatorios.

**Interpretación:**
- **Correlación < 0.8:** Posible manipulación esteganográfica
- **Correlación > 0.95:** Imagen probablemente no modificada
- Se calcula en direcciones horizontal y vertical

---

####  Runs Test (Test de Rachas)
Evalúa la secuencialidad de bits LSB. En secuencias aleatorias, el número de "rachas" (transiciones 0→1 o 1→0) sigue una distribución predecible. Desviaciones sugieren patrones artificiales.

**Interpretación:**
- **|z-score| > 2:** Secuencia no aleatoria (p-valor < 0.05)
- **p-valor < 0.05:** Rechaza hipótesis de aleatoriedad

---

### Puntuación de Sospecha Combinada

El sistema integra todas las métricas anteriores en una puntuación ponderada (0.0 - 1.0):

```
Puntuación = 0.4×(χ² sospechoso) + 0.2×(desviación de media) + 
             0.2×(entropía alta) + 0.2×(correlación baja)
```

**Umbrales:**
- **< 0.3:** Imagen limpia
- **0.3 - 0.6:** Sospechosa (requiere análisis manual)
- **> 0.6:** Alta probabilidad de esteganografía

---


---

## 👥 Equipo Snoopy

Desarrollado con 💜 por el Equipo Snoopy
- Jennifer Patricia Valencia Ignacio, Código: 223991721
- Elizabeth Arroyo Moreno, Código: 221453749 
- Karla Rebeca Hernández Elizarrarás, Código: 223991977

---

# Referencias

### Esteganografía y LSB
- Kaspersky. (2023, febrero 8). *¿Qué es la esteganografía? ¿Cómo funciona?* https://latam.kaspersky.com/resource-center/definitions/what-is-steganography

- Lenovo. (s.f.). *¿Qué es el Bit Menos Significativo y Cómo Afecta a la Manipulación de Datos?* Recuperado el 27 de noviembre de 2025, de https://www.lenovo.com/es/es/glossary/least-significant-bit/

### Algoritmos Implementados
- Casero, A. (2023, diciembre 13). *¿Qué es el algoritmo de fuerza bruta en programación?* KeepCoding Bootcamps. https://keepcoding.io/blog/algoritmo-de-fuerza-bruta-en-programacion/

- freeCodeCamp. (2020, enero 6). *Brute Force Algorithms explained.* https://www.freecodecamp.org/news/brute-force-algorithms-explained/

- García, D. C. (s.f.). *La recursividad y el algoritmo de divide y vencerás.* Medium. Recuperado el 27 de noviembre de 2025, de https://medium.com/@davidcabreraygarcia/la-recursividad-y-el-algoritmo-de-divide-y-vencerás-9418325e55b5

- Martínez, J. E. (2020, junio 10). *Algoritmia: Divide y vencerás.* Adictos al trabajo. https://adictosaltrabajo.com/2020/06/10/algoritmia-divide-y-venceras/

- Nb, T. H. A. (2023, mayo 12). *What is a Greedy Algorithm? Examples of Greedy Algorithms.* freeCodeCamp. https://www.freecodecamp.org/news/greedy-algorithms/

---


