# Detector-B-sico-de-Tapabocas-con-OpenCV
Este proyecto implementa un sistema básico de detección de tapabocas 
utilizando visión por computador con OpenCV en Python.

El sistema analiza el rostro detectado por la cámara web y determina 
si existe una posible obstrucción en la zona de nariz y boca, basándose 
en detección facial y análisis de color.

## Tecnologías utilizadas

- Python 3.x
- OpenCV
- NumPy
- Tkinter
- Haar Cascades (detección facial)

## Requisitos

- Python 3.9 o superior
- Cámara web funcional

## Instalación

1. Clonar el repositorio:

git clone https://github.com/portadordelaluz/Detector-B-sico-de-Tapabocas-con-OpenCV

2. Entrar a la carpeta del proyecto:

cd turepositorio

3. Crear entorno virtual (opcional pero recomendado):

python -m venv venv
venv\Scripts\activate

4. Instalar dependencias:

pip install -r requirements.txt

## Ejecución

Para ejecutar el programa:

python main.py

## Funcionamiento

- Al ejecutar el programa, se abrirá una ventana con la cámara activa.
- Si se detecta un rostro:
  - Si se identifican nariz y boca → se muestra "Sin tapabocas".
  - Si no se detectan → se muestra "Posible tapabocas".
- El botón "Salir" cierra completamente el programa.
 
## Limitaciones

- La detección funciona mejor con el rostro de frente.
- Puede presentar falsos positivos con iluminación baja.
- No utiliza modelos de deep learning, sino clasificadores Haar.

## Autor

Keiler Ferrer Hurtado 
20251020104
Ingeniería de sistemas
Universidad Distrital
