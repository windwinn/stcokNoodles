from sqlalchemy.orm import Session
from database import SessionLocal
import models

freshFoods = [
    {
        "name": "บะหมี่",
        "remain_unit": "ถุง",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "แผ่นเกี๊ยวต้ม",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "แผ่นเกี๊ยวทอด",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "เกี๊ยวหมู",
        "remain_unit": "ถุง",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "เกี๊ยวกุ้ง",
        "remain_unit": "ชุด",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "หมูแดง",
        "remain_unit": "เส้น",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ปู",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ไก่ข้าวผัด",
        "remain_unit": "ถุง",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กุ้งข้าวผัด",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กระดูกเล้ง",
        "remain_unit": "วัน",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กระดูกข้อ",
        "remain_unit": "วัน",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กากหมู",
        "remain_unit": "วัน",
        "order_unit": "ชุด",
        "category": "FF",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กวางตุ้ง",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ต้นหอม",
        "remain_unit": "กิโลกรัม",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "พริกชิ้ฟ้า",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "กระเทียม",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ฝัก",
        "remain_unit": "ลูก",
        "order_unit": "ลูก",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "แครอท",
        "remain_unit": "หัว",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "หอมใหญ่",
        "remain_unit": "หัว",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "แตงล้าน",
        "remain_unit": "ลูก",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "พริกขี้หนู",
        "remain_unit": "ถุง",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "มะนาว",
        "remain_unit": "ถุง",
        "order_unit": "ถุง",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ใบเตย",
        "remain_unit": "มัด",
        "order_unit": "มัด",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "มะพร้าว",
        "remain_unit": "ลูก",
        "order_unit": "ลูก",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    },
    {
        "name": "ลำไย",
        "remain_unit": "ถุง",
        "order_unit": "กิโลกรัม",
        "category": "VT",
        "note": "",
        "order": "0",
        "remain": None,
        "visible_item": True
    }
]


db: Session = SessionLocal()

for item in freshFoods:
    product = models.MasterProduct(**item)
    db.add(product)

db.commit()
print("Seed completed.")