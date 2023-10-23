from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:197300@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         connection = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '197300',cursor_factory=psycopg2.extras.RealDictCursor)
#         cursor = connection.cursor()
#         print("Succesfully connected to the Database")
#         break

#     except Exception as error:

#         print("Truble Connecting to the Database")
#         print(error)
#         time.sleep(3)
