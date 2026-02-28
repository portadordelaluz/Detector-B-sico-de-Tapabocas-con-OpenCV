import cv2
import numpy as np

# Cargar clasificador de rostros
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Iniciar cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Dibujar rectángulo en rostro
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Región inferior del rostro (donde estaría el tapabocas)
        lower_face = gray[y + h//2:y + h, x:x + w]
        
        # Calcular promedio de intensidad
        mean_intensity = np.mean(lower_face)

        if mean_intensity < 100:
            text = "Posible tapabocas"
            color = (0, 255, 0)
        else:
            text = "Sin tapabocas"
            color = (0, 0, 255)

        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Detector Tapabocas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
