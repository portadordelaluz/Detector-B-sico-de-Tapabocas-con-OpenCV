import cv2
import numpy as np
import tkinter as tk
import threading

running = False
cap = None

def iniciar_camara():
    global running
    if running:
        return
    running = True
    estado_label.config(text="Estado: ACTIVO", fg="green")

    hilo = threading.Thread(target=camara, daemon=True)
    hilo.start()

def detener_camara():
    global running
    running = False

def camara():
    global running, cap

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            lower_color = hsv[y + int(h*0.5):y + h, x:x + w]
            lower_gray = gray[y + int(h*0.5):y + h, x:x + w]

            lower_blue = np.array([90, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask_blue = cv2.inRange(lower_color, lower_blue, upper_blue)

            lower_black = np.array([0, 0, 0])
            upper_black = np.array([180, 255, 60])
            mask_black = cv2.inRange(lower_color, lower_black, upper_black)

            blue_pixels = cv2.countNonZero(mask_blue)
            black_pixels = cv2.countNonZero(mask_black)

            mouths = mouth_cascade.detectMultiScale(lower_gray, 1.7, 20)

            area = lower_color.shape[0] * lower_color.shape[1]
            blue_ratio = blue_pixels / area
            black_ratio = black_pixels / area

            if (blue_ratio > 0.25 or black_ratio > 0.30) and len(mouths) == 0:
                text = "Tapabocas Detectado"
                color = (0, 255, 0)
            else:
                text = "Sin Tapabocas"
                color = (0, 0, 255)

            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("Detector Inteligente de Tapabocas", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

    liberar_recursos()

def liberar_recursos():
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    estado_label.config(text="Estado: DETENIDO", fg="red")

def salir():
    global running
    running = False
    liberar_recursos()
    ventana.destroy()


ventana = tk.Tk()
ventana.title("Detector Inteligente de Tapabocas")
ventana.geometry("350x220")
ventana.configure(bg="#f0f0f0")

titulo = tk.Label(ventana, text="Sistema de Detección de Tapabocas",
                  font=("Arial", 13, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

estado_label = tk.Label(ventana, text="Estado: DETENIDO",
                        font=("Arial", 11), fg="red", bg="#f0f0f0")
estado_label.pack(pady=5)

btn_iniciar = tk.Button(ventana, text="Iniciar Cámara",
                        command=iniciar_camara, width=25, bg="#4CAF50", fg="white")
btn_iniciar.pack(pady=5)

btn_detener = tk.Button(ventana, text="Detener Cámara",
                        command=detener_camara, width=25, bg="#f39c12", fg="white")
btn_detener.pack(pady=5)

btn_salir = tk.Button(ventana, text="Salir",
                      command=salir, width=25, bg="#e74c3c", fg="white")
btn_salir.pack(pady=5)

ventana.protocol("WM_DELETE_WINDOW", salir)

ventana.mainloop()
