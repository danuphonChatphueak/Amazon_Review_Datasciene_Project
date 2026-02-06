import pandas as pd
import re

# อ่านไฟล์ excel
df = pd.read_excel("10.synthetic_amazon_like_reviews_3class_hard_5000.xlsx")

# ชื่อ column ที่ต้องการแก้
col = "text"

df[col] = (
    df[col]
    .astype(str)                 # กัน error ถ้ามี NaN
    .str.lower()                 # แปลงเป็นพิมพ์เล็ก
    .str.replace(r"\s+", " ", regex=True)  # รวมช่องว่างหลายตัวเป็น 1
    .str.strip()                 # ลบช่องว่างหน้า-หลัง
)

# บันทึกไฟล์ใหม่
df.to_excel("output_clean.xlsx", index=False)
