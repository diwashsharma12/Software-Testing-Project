from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, Float

# -----------------------------------
# MYSQL CONNECTION
# -----------------------------------

DATABASE_URL = "mysql+pymysql://root:hello123@localhost/add_app_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# -----------------------------------
# TABLE MODEL
# -----------------------------------

class Calculation(Base):

    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)

    number1 = Column(Float)

    number2 = Column(Float)

    result = Column(Float)

# Create table automatically
Base.metadata.create_all(bind=engine)

# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# HOME
# -----------------------------------

@app.get("/")
def home():
    return {"message": "API Running"}

# -----------------------------------
# ADD NUMBERS
# -----------------------------------

@app.get("/add")
def add_numbers(a: float, b: float):

    result = a + b

    db = SessionLocal()

    calculation = Calculation(
        number1=a,
        number2=b,
        result=result
    )

    db.add(calculation)

    db.commit()

    db.close()

    return {"result": result}

# -----------------------------------
# GET HISTORY
# -----------------------------------

@app.get("/history")
def history():

    db = SessionLocal()

    calculations = db.query(Calculation).all()

    data = []

    for item in calculations:

        data.append({
            "id": item.id,
            "number1": item.number1,
            "number2": item.number2,
            "result": item.result
        })

    db.close()

    return data