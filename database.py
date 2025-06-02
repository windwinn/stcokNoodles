from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:yeeStock15@eipmouvlllqdagdfqrhv.supabase.co:5432/postgres"

DATABASE_URL = (
    "postgresql://postgres.eipmouvlllqdagdfqrhv:yeeStock15"
    "@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
    "?options=--cluster%3Ddb-eipmouvlllqdagdfqrhv&sslmode=require&gssencmode=disable"
)

engine = create_engine(DATABASE_URL,connect_args={
    "sslmode": "require",
    "gssencmode": "disable",
})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

