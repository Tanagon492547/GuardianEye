import cv2
import numpy as np
from ultralytics import YOLO
from django.shortcuts import render
from django.http import StreamingHttpResponse
import pickle
import os
from django.conf import settings # import settings เพื่อหาตำแหน่งไฟล์

# --- ส่วนของโค้ด YOLO และการประมวลผลวิดีโอ ---

# 1. โหลดโมเดล .pickle ที่เราบันทึกไว้
print(">>> [ขั้นตอนที่ 1] กำลังโหลดโมเดล GuardianEye.pickle...")
model = None # กำหนดค่าเริ่มต้นให้เป็น None
try:
    # สร้าง path ไปยังโมเดลที่อยู่ในโฟลเดอร์เดียวกับ views.py
    # settings.BASE_DIR คือ path ของโฟลเดอร์โปรเจกต์หลัก (ที่มี manage.py)
    model_path = os.path.join(settings.BASE_DIR, 'GuardianEye', 'GuardianEye.pickle')

    if not os.path.exists(model_path):
            raise FileNotFoundError(f"หาไฟล์โมเดลไม่เจอที่: {model_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        
    print(f"+++ โหลดโมเดลจาก {model_path} สำเร็จ!")
    
except Exception as e:
    print(f"--- เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")


def generate_frames():
    """
    ฟังก์ชัน Generator ที่จะอ่านภาพจากกล้อง, ประมวลผลด้วย YOLO,
    และส่ง (yield) ภาพผลลัพธ์ออกมาทีละเฟรม
    """
    print(">>> [ขั้นตอนที่ 2] กำลังพยายามเปิดกล้องเว็บแคม...")
    cap = cv2.VideoCapture(0)
    
    # ตรวจสอบว่าเปิดกล้องได้ไหม และ โหลดโมเดลสำเร็จหรือยัง
    if not cap.isOpened() or model is None:
        if not cap.isOpened():
            print("--- ไม่สามารถเปิดกล้องเว็บแคมได้")
        if model is None:
            print("--- ไม่สามารถใช้งานโมเดลได้ (โหลดไม่สำเร็จ)")

        # สร้างภาพ Error ขึ้นมาเอง
        error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(error_frame, "Error: Cannot access webcam or model.", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        ret, buffer = cv2.imencode('.jpg', error_frame)
        frame_bytes = buffer.tobytes()
        # ส่งภาพ Error ออกไปแล้วจบการทำงาน
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        return
    
    print("+++ เปิดกล้องเว็บแคมสำเร็จ! เริ่มการสตรีม...")
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # ประมวลผลภาพด้วยโมเดล YOLO
            results = model(frame, stream=True, verbose=False)

            # วาดกรอบและข้อความลงบนเฟรมภาพ
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = round(float(box.conf[0]), 2)
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    
                    label = f'{class_name} {conf}'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # แปลงเฟรมภาพเป็น JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # ส่งเฟรมภาพออกไปสำหรับ Streaming
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    print("--- หยุดการสตรีมแล้ว")
    cap.release()

# --- ส่วนของ Django Views ---

def video_feed(request):
    """
    View ที่ทำหน้าที่สตรีมวิดีโอจากฟังก์ชัน generate_frames
    """
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    """
    View ที่แสดงหน้าเว็บหลักโดยการโหลดไฟล์ index.html
    """
    return render(request, 'GuardianEye/index.html')

