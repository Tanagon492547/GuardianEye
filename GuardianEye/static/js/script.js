// รอให้หน้าเว็บโหลดเสร็จก่อน
document.addEventListener('DOMContentLoaded', () => {

    const h1 = document.querySelector('h1');

    if (h1) {
        const text = h1.textContent;
        // ล้างข้อความเดิมใน h1
        h1.textContent = ''; 

        // แยกข้อความออกเป็นแต่ละตัวอักษร แล้วสร้างเป็น <span> tag
        text.split('').forEach((letter, index) => {
            const span = document.createElement('span');
            span.textContent = letter;

            // แก้ปัญหาตัวอักษรที่เป็นช่องว่าง
            if(letter === ' '){
                span.style.margin = '0 0.2em';
            }

            // นี่คือหัวใจสำคัญ! เราจะหน่วงเวลาอนิเมชันของแต่ละตัวอักษร
            // เพื่อสร้างเอฟเฟกต์ "คลื่น" ที่สวยงาม
            span.style.animationDelay = `${index * 0.1}s`;

            h1.appendChild(span);
        });
    }

});

