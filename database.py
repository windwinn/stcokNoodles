import os
from dotenv import load_dotenv  # <-- ถ้ายังไม่มี

load_dotenv()  # โหลดจากไฟล์ .env
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# DATABASE_URL = "postgresql://postgres:yeeStock15@eipmouvlllqdagdfqrhv.supabase.co:5432/postgres"

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL,connect_args={
    "sslmode": "require",
    "gssencmode": "disable",
})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

