from sqlalchemy.orm import Session
from database import SessionLocal
import models

units = [
    {"name": "กิโลกรัม", "code": "KG"},
    {"name": "ถุง", "code": "BAG"},
    {"name": "ลูก", "code": "L"},
    {"name": "เส้น", "code": "LINE"},
    {"name": "ชุด", "code": "MEAL"},
    {"name": "วัน", "code": "DAY"},
    {"name": "หัว", "code": "PATE"},
    {"name": "มัด", "code": "BUNDLE"},
    {"name": "แผง", "code": "PANEL"},
]

db: Session = SessionLocal()

for item in units:
    Unit = models.MasterUnit(**item)
    db.add(Unit)

db.commit()
print("Seed completed.")