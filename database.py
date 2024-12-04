from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:@localhost:5432/eventology_db"
DATABASE_URL = "postgresql://eventology_db_owner:YXeow01pgUAH@ep-rapid-brook-a55mgqfg.us-east-2.aws.neon.tech/eventology_db?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)