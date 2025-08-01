import cv2
import torch
import serial

# โหลดโมเดล YOLO
model = torch.hub.load('ultralytics/yolov', 'custom', path='best.pt')

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# เชื่อมต่อกับ Arduino
arduino = serial.Serial('COM3', 9600)

while True:
    ret, frame = cap.read()
    results = model(frame)

    # ตรวจจับว่าเจอวัตถุที่ต้องการหรือไม่
    for obj in results.pred[0]:
        cls = int(obj[5])
        if cls == 0:  # สมมติว่า class 0 คือ "คน"
            arduino.write(b'1')  # ส่ง '1' ไป Arduino
        else:
            arduino.write(b'0')  # ส่ง '0'

    # แสดงภาพ
    cv2.imshow('Frame', results.render()[0])
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
