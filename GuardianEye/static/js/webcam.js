// webcam.js

window.onload = function() {
    // --- โค้ดสำหรับแอนิเมชันตัวอักษร ---
    const heading = document.querySelector('h1');
    const text = heading.textContent;
    let index = 0;

    // สร้าง <span> ครอบแต่ละตัวอักษร
    heading.innerHTML = '';
    for (let i = 0; i < text.length; i++) {
        const span = document.createElement('span');
        span.textContent = text[i];
        heading.appendChild(span);
    }

    const spans = heading.querySelectorAll('span');

    // ตั้งค่า Interval สำหรับแอนิเมชันตัวอักษร
    setInterval(() => {
        spans.forEach(span => span.classList.remove('large'));
        spans[index].classList.add('large');
        index = (index + 1) % spans.length;
    }, 500);

    // --- จบโค้ดแอนิเมชันตัวอักษร ---

    // โค้ดสำหรับเว็บแคม
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('detection-canvas'); // เปลี่ยนตรงนี้
    const context = canvas.getContext('2d');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            video.srcObject = stream;
        })
        .catch(function(error) {
            console.error("เกิดข้อผิดพลาดในการเข้าถึงกล้อง:", error);
            alert("ไม่สามารถเข้าถึงกล้องได้ โปรดตรวจสอบการตั้งค่าเบราว์เซอร์เหมียว");
        });
    }

    video.addEventListener('loadedmetadata', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
    });

    const csrfToken = document.body.dataset.csrftoken;

    setInterval(() => {
        // วาดภาพวิดีโอลงบน canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        fetch('/detect/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ image: imageData }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('ผลลัพธ์จากโมเดล:', data);
            
            // เพิ่มโค้ดส่วนนี้เพื่อวาดกรอบลงบน canvas
            context.clearRect(0, 0, canvas.width, canvas.height); // ล้าง canvas ทุกครั้งที่วาดใหม่
            
            if (data.results && data.results.length > 0) {
                data.results.forEach(result => {
                    const [x_min, y_min, x_max, y_max, confidence, class_id] = result;

                    // วาดกรอบสี่เหลี่ยม
                    context.beginPath();
                    context.lineWidth = "4";
                    context.strokeStyle = "red"; // สีของกรอบ
                    context.rect(x_min, y_min, x_max - x_min, y_max - y_min);
                    context.stroke();

                    // วาดข้อความ
                    context.font = "bold 18px Arial";
                    context.fillStyle = "red";
                    context.fillText(`Class: ${class_id} (${(confidence * 100).toFixed(2)}%)`, x_min, y_min - 10);
                });
            }
        })
        .catch(error => {
            console.error('เกิดข้อผิดพลาดในการส่งข้อมูล:', error);
        });
    }, 200);
};