from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
DATABASE_URL = "postgresql://rul_user:12345678@localhost/rul_db"
 
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)
 
# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# Create a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()