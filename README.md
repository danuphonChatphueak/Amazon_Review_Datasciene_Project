วิธีรัน 

1.รันส่วน backend 

ใช้คำสั่ง  

cd backend

pip install requirement.txt

uvicorn main:app --reload --host 0.0.0.0 port 8000

2.รันหน้าเว็บ ที่ไฟล์ index.html

วิธี deploy

1.อัพไฟล์โปรแกรมขึ้นบน git repo

2.เปิด render เพื่อ deploy

3.สร้าง web service แล้วเชื่อมต่อกับ gitrepo

4.ตั้งค่าการ deploy 

root directory:

Build Command :python -m pip install -r backend/requirements.txt

Start Command : bash backend/start.sh

กด deploy

5.deployหน้าเว็บ สร้าง Static Site แล้วเชื่อมต่อกับ git repo

6.ตั้งค่าการ deploy 

root directory:

Build Command :

Publish Directory : Frontend

กด deploy
