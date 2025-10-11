FROM python:3.9-slim

WORKDIR /app

# ตั้งค่าสภาพแวดล้อม
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดโปรเจค
COPY . .

# สร้างโฟลเดอร์สำหรับเก็บไฟล์มีเดีย
RUN mkdir -p /app/media/images

# เปิดพอร์ต
EXPOSE 8000

# รันเซิร์ฟเวอร์
CMD ["python", "storage_microservice/manage.py", "runserver", "0.0.0.0:8000"]