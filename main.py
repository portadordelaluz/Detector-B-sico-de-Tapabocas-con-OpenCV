import cv2
import tkinter as tk
import threading
import sys

running = False
cap = None
contador_estable = 0
buffer_frames = 0

face_frontal = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_profile = cv2.CascadeClassifier("haarcascade_profileface.xml")

def iniciar_camara():
    global running
    if running:
        return
    running = True
    estado_label.config(text="Estado: ACTIVO", fg="green")
    threading.Thread(target=camara, daemon=True).start()

def detener_camara():
    global running, cap
    running = False
    if cap is not None:
        cap.release()
        cap = None
    cv2.destroyAllWindows()
    estado_label.config(text="Estado: INACTIVO", fg="red")

def cerrar_programa():
    detener_camara()
    ventana.destroy()
    sys.exit()

def eliminar_duplicados(cajas):
    resultado = []
    for (x, y, w, h) in cajas:
        duplicado = False
        for (x2, y2, w2, h2) in resultado:
            if abs(x - x2) < 60 and abs(y - y2) < 60:
                duplicado = True
                break
        if not duplicado:
            resultado.append((x, y, w, h))
    return resultado

def camara():
    global cap, running, contador_estable, buffer_frames

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    cajas_final = []

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if frame_count % 2 == 0:

            cajas = []

            frontal = face_frontal.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60,60)
            )

            perfil = face_profile.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60,60)
            )

            flipped = cv2.flip(gray, 1)
            perfil_flip = face_profile.detectMultiScale(
                flipped,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60,60)
            )

            for (x,y,w,h) in frontal:
                cajas.append((x,y,w,h))

            for (x,y,w,h) in perfil:
                cajas.append((x,y,w,h))

            for (x,y,w,h) in perfil_flip:
                x = gray.shape[1] - x - w
                cajas.append((x,y,w,h))

            cajas = eliminar_duplicados(cajas)

            cajas_final = []
            for (x,y,w,h) in cajas:
                x = int(x / 0.5)
                y = int(y / 0.5)
                w = int(w / 0.5)
                h = int(h / 0.5)
                cajas_final.append((x,y,w,h))

            detecciones = len(cajas_final)

            if detecciones > 0:
                contador_estable = detecciones
                buffer_frames = 0
            else:
                buffer_frames += 1
                if buffer_frames > 10:
                    contador_estable = 0

        for (x,y,w,h) in cajas_final:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

        cv2.putText(frame,
                    f"Personas: {contador_estable}",
                    (frame.shape[1]-220, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2)

        cv2.imshow("Contador de Personas", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    detener_camara()

ventana = tk.Tk()
ventana.title("Contador de Personas")
ventana.geometry("300x200")
ventana.resizable(False, False)

tk.Label(ventana, text="Contador de Personas",
         font=("Arial", 14)).pack(pady=10)

estado_label = tk.Label(ventana,
                        text="Estado: INACTIVO",
                        fg="red",
                        font=("Arial", 12))
estado_label.pack(pady=5)

tk.Button(ventana, text="Iniciar Camara",
          command=iniciar_camara, width=20).pack(pady=5)

tk.Button(ventana, text="Detener Camara",
          command=detener_camara, width=20).pack(pady=5)

tk.Button(ventana, text="Salir",
          command=cerrar_programa, width=20).pack(pady=10)

ventana.protocol("WM_DELETE_WINDOW", cerrar_programa)

ventana.mainloop()
