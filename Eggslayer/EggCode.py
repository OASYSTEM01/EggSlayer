import cv2
import torch
import serial
import serial.tools.list_ports
from ultralytics import YOLO

model = YOLO('C:/Users/Focus/Desktop/EggSlayer/Eggslayer/my_model/train/weights/best.pt')  # โหลดโมเดล

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# เชื่อมต่อกับ Arduino แบบอัตโนมัติ
ports = list(serial.tools.list_ports.comports())
for p in ports:
     if "Arduino" in p.description:
        print(f"Arduino found on {p.device}")
        arduino = serial.Serial(p.device, 9600)
        break
     else:
        raise IOError("Arduino not found.")

while True:
    ret, frame = cap.read()  
    if not ret:
        break

    results = model(frame)
    annotated_frame = results[0].plot()

    cv2.imshow('Frame', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # ตรวจจับวัตถุจาก results[0].boxes
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if cls == 0 :  
            arduino.write(b'1')
        else:
            arduino.write(b'0')
    
    

cap.release()
cv2.destroyAllWindows()
