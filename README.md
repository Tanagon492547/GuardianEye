# **👁️ Project GuardianEye \- Real-time Detection System**

ยินดีต้อนรับสู่โปรเจกต์ GuardianEye\! นี่คือเว็บแอปพลิเคชันสำหรับตรวจจับวัตถุแบบเรียลไทม์ผ่านกล้องเว็บแคม สร้างขึ้นด้วย Django และ YOLOv8

## **✨ คุณสมบัติหลัก**

* **Real-time Detection**: ตรวจจับวัตถุจากวิดีโอสตรีมของเว็บแคมแบบสดๆ  
* **Web Interface**: แสดงผลลัพธ์ผ่านหน้าเว็บเบราว์เซอร์ที่สวยงามและใช้งานง่าย  
* **Custom Model**: สามารถเปลี่ยนไปใช้โมเดล .pt หรือ .pickle ที่คุณเทรนเองได้อย่างง่ายดาย  
* **Scalable**: สร้างขึ้นบนโครงสร้างโปรเจกต์ Django ที่เป็นมาตรฐาน ง่ายต่อการพัฒนาและต่อยอด

## **🚀 เริ่มต้นใช้งาน (Getting Started)**

ทำตามขั้นตอนง่ายๆ เหล่านี้เพื่อรันโปรเจกต์บนเครื่องของคุณ

### **1\. โคลนโปรเจกต์ (Clone the Repository)**

```bash

git clone \<your-repository-url\>  
cd ProjectGuardianEye

```

### **2\. สร้างสภาพแวดล้อมเสมือน (Create a Virtual Environment)**

แนะนำให้สร้าง Virtual Environment เพื่อแยกไลบรารีของโปรเจกต์นี้ออกจากโปรเจกต์อื่นๆ

\# สำหรับ Windows  

python \-m venv GuardianEye  
GuardianEye\\Scripts\\activate

\# สำหรับ macOS/Linux  
python3 \-m venv GuardianEye  
source GuardianEye/bin/activate

### **3\. ติดตั้งไลบรารีที่จำเป็น (Install Dependencies)**

เราได้เตรียมไฟล์ requirements.txt ไว้ให้แล้ว คุณสามารถติดตั้งทุกอย่างได้ในคำสั่งเดียว

```bash

pip install \-r requirements.txt

```

### **4\. รันเซิร์ฟเวอร์ (Run the Development Server)**

เมื่อติดตั้งทุกอย่างเสร็จเรียบร้อย ก็ถึงเวลารันโปรเจกต์\!

```bash

python manage.py runserver

```

จากนั้นเปิดเว็บเบราว์เซอร์แล้วไปที่ http://127.0.0.1:8000/ คุณจะเห็นหน้าเว็บ GuardianEye พร้อมวิดีโอสตรีมจากกล้องของคุณ\!

## **📂 โครงสร้างโปรเจกต์**

PROJECTGUARDIANEYE/  
├── GuardianEye/              \# โฟลเดอร์ของแอปพลิเคชันหลัก  
│   ├── static/               \# เก็บไฟล์ CSS, JS, Images  
│   ├── templates/            \# เก็บไฟล์ HTML  
│   ├── \_\_init\_\_.py  
│   ├── models.py  
│   ├── urls.py               \# สารบัญของแอป  
│   ├── views.py              \# โค้ดหลักทั้งหมดอยู่ที่นี่\!  
│   └── ...  
├── ProjectGuardianEye/       \# โฟลเดอร์สำหรับตั้งค่าโปรเจกต์  
│   ├── \_\_init\_\_.py  
│   ├── settings.py           \# ไฟล์ตั้งค่าหลักของ Django  
│   ├── urls.py               \# สารบัญหลักของโปรเจกต์  
│   └── ...  
├── GuardianEye.pickle        \# ไฟล์โมเดลของคุณ  
├── manage.py                 \# กุญแจสตาร์ทโปรเจกต์  
└── requirements.txt          \# รายชื่อไลบรารีที่ต้องใช้

ขอให้สนุกกับการพัฒนาโปรเจกต์นะ\! 🐱