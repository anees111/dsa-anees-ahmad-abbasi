from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
DATABASE_URL = "postgresql://postgres:Anees12345@localhost/mydatabase"
 
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