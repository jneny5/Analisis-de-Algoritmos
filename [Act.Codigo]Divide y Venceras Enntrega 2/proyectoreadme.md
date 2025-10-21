# Detector de Mensajes Ocultos en Imágenes

¿Sabías que puedes esconder mensajes secretos en imágenes? Este programa detecta y extrae esos mensajes ocultos usando una técnica llamada LSB.

## ¿Qué hace?

- Encuentra mensajes secretos escondidos en imágenes
- Compara dos formas diferentes de buscar (Fuerza Bruta vs Divide y Vencerás)
- Te dice qué tan sospechosa es una imagen
- Crea imágenes con mensajes ocultos
- Hace gráficas bonitas para ver qué método es más rápido

## Instalación

Necesitas Python y algunas librerías. Instálalas así:

```bash
pip install opencv-python numpy Pillow matplotlib scipy
```

## Cómo usarlo

Simplemente corre el programa:

```bash
python comparativa_LSB.py
```

Te va a salir un menú con 5 opciones:

1. **Analizar imagen** - Busca mensajes ocultos y te da estadísticas
2. **Crear imagen nueva** - Hace una imagen con tu mensaje secreto
3. **Ocultar mensaje** - Esconde un mensaje en una foto que ya tengas
4. **Comparar velocidad** - Ve qué método es más rápido
5. **Salir** - Cierra el programa

## Ejemplos de uso

### Buscar mensajes ocultos

Elige la opción 1, selecciona tu imagen, y el programa te dirá:
- Si encontró algo
- Cuánto tardó en buscar
- Qué tan sospechosa es la imagen (de 0 a 1)

```
MENSAJE ENCONTRADO: 'Hola Mundo'
Tiempo: 0.002 segundos
Puntuación de sospecha: 0.85/1.0
Estado: ESTEGANOGRAFÍA DETECTADA
```

### Crear tu propia imagen con mensaje

Usa la opción 2 para crear una imagen nueva con tu mensaje secreto. ¡Nadie sabrá que está ahí!

### Comparar métodos

La opción 4 hace pruebas con imágenes de diferentes tamaños y crea gráficas que muestran:
- Cuál método es más rápido
- Cuánto tiempo ahorra cada uno
- Cómo cambia la velocidad según el tamaño de la imagen

## Los dos métodos

**Fuerza Bruta:** Revisa todos los píxeles uno por uno, del principio al final.

**Divide y Vencerás:** Divide la imagen en pedazos más chicos y los revisa por partes. ¡Normalmente es más rápido!

## Cosas importantes

- Solo funciona con el canal rojo de la imagen
- El mensaje debe terminar con "END"
- Funciona mejor con imágenes PNG (no tanto con JPEG)

## Lo que hace especial

Aunque ambos métodos hacen lo mismo, Divide y Vencerás suele ser más rápido porque aprovecha mejor la memoria de tu computadora.

## Gráficas que crea

Cuando haces el benchmark, el programa guarda 6 gráficas en una carpeta:
1. Comparación de tiempos
2. Escala logarítmica
3. Qué tan más rápido es uno que otro
4. Porcentaje de mejora
5. Análisis de cada método

