from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import uvicorn
from fastapi import Form
import os
from dotenv import load_dotenv

# This looks for a file named .env in your project folder
load_dotenv()

# Now you can access your secrets like this:
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

import joblib
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths
transformer_path = os.path.join(base_dir, "models", "column_transformer.pkl")
main_model_path = os.path.join(base_dir, "models", "main_property_model.pkl")
portions_model_path = os.path.join(base_dir, "models", "portions_model.pkl")

# Load them
transformer = joblib.load(transformer_path)
main_model = joblib.load(main_model_path)
portions_model = joblib.load(portions_model_path)

print("Successfully loaded AI models!")

import joblib
import pandas as pd
from fastapi import HTTPException

# 1. Load the models AND the transformer at startup
transformer = joblib.load("models/column_transformer.pkl")
main_model = joblib.load("models/main_property_model.pkl")
portions_model = joblib.load("models/portions_model.pkl")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse

@app.get("/")
async def home():
    return FileResponse("templates/index.html")
# ... after you define app = FastAPI() ...

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_ORIGIN", "*")],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.get("/healthz")
async def health():
    return {"status": "ok"}

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()
# Path to the .db file your friend sent
db_path = r"C:\Users\Humma\OneDrive\Desktop\python projects\karachi_housing.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
# This creates the link between your Class and the Database file
Base.metadata.create_all(bind=engine)

from pydantic import BaseModel

from sqlalchemy import inspect


class PropertyDB(Base):
   
    __tablename__ = "main_properties"

    property_id = Column(Integer, primary_key=True, autoincrement=True)
    property_type = Column(String)
    # ignore 'price' and use 'final_price'
    final_price = Column(Float)
    location = Column(String)
    bathrooms = Column(Integer)
    bedrooms = Column(Integer)
    purpose = Column(String)
    area_sq_feet = Column(Float)
    area_sq_yards = Column(Float)

# Note: In your code, when you want to access the price,
# always use 'property.final_price' instead of 'property.price'.

class SizeUnitEnum(str, Enum):
    sq_yrd = "sq_yrd"
    sq_ft = "sq_ft"
    class Config:
        from_attributes = True

class PurposeEnum(str, Enum):
    rent = "rent"
    purchase = "purchase"
    class Config:
        from_attributes = True

class PropertyTypeEnum(str, Enum):
    upper_portion = "upper_portion"
    lower_portion = "lower_portion"
    house = "house"
    apartment = "apartment"
    class Config:
        from_attributes = True

class PropertyUpdate(BaseModel):
    property_id: int= Field(...)
    location: Optional[str] = None
    size: Optional[float] = None
    final_price: float = Field (...)
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    property_type: Optional[PropertyTypeEnum] = None
    purpose: Optional[PurposeEnum] = None
    unit: Optional[SizeUnitEnum] = None
    class Config:
        from_attributes = True

class AIInput(BaseModel):
    location: str
    property_type: str
    purpose: str
    bathrooms: str
    bedrooms: str
    area_sq_yards: str

class Property(BaseModel):
    property_id: int
    property_type: str
    location: str
    bathrooms: int
    purpose: str
    bedrooms: int
    area_sq_feet: float
    area_sq_yards: float
    final_price: float

    class Config:
        from_attributes = True

Property.model_rebuild()

@app.post("/predict_price")
async def predict_price(data: AIInput):
    # Convert to title case before creating the DataFrame
    location = data.location.strip().title()
    try:
        baths = int(data.bathrooms) if data.bathrooms and str(data.bathrooms).strip() != "" else 0
        beds = int(data.bedrooms) if data.bedrooms and str(data.bedrooms).strip() != "" else 0
        yards = float(data.area_sq_yards) if data.area_sq_yards and str(data.area_sq_yards).strip() != "" else 0.0
    except ValueError:
        return {"error": "Please ensure numeric properties (Beds, Baths, Yards) contain clean numbers."}
    # This creates a dictionary directly from the data received
    input_dict = {
        'location': location,
        'bathrooms': baths,
        'bedrooms': beds,
        'purpose': data.purpose,
        'property_type': data.property_type,
        'area_sq_yards': yards
    }
   
    # Create the DataFrame
    input_df = pd.DataFrame([input_dict])
   
    # Transform and Predict
    try:
        processed_data = transformer.transform(input_df)
        prediction = main_model.predict(processed_data)
        return {"predicted_price": float(prediction[0])}
    except Exception as e:
        return {"error": str(e)}



engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
       
# --- SEARCH & FILTER
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/properties")
def get_properties(
    db: Session = Depends(get_db),
    area: str = None,
    purpose: str = None,
    property_type: str = None,
    min_price: str = None,
    max_price: str = None,
    bedrooms: str = None,
    bathrooms: str = None,
    min_sq_feet: str = None,
    max_sq_feet: str = None,
    min_sq_yards: str = None,
    max_sq_yards: str = None,
):
    min_price = int(min_price) if min_price and str(min_price).strip() != "" else None
    max_price = int(max_price) if max_price and str(max_price).strip() != "" else None
    bedrooms = int(bedrooms) if bedrooms and str(bedrooms).strip() != "" else None
    bathrooms = int(bathrooms) if bathrooms and str(bathrooms).strip() != "" else None
    min_sq_feet = float(min_sq_feet) if min_sq_feet and str(min_sq_feet).strip() != "" else None
    max_sq_feet = float(max_sq_feet) if max_sq_feet and str(max_sq_feet).strip() != "" else None
    min_sq_yards = float(min_sq_yards) if min_sq_yards and str(min_sq_yards).strip() != "" else None
    max_sq_yards = float(max_sq_yards) if max_sq_yards and str(max_sq_yards).strip() != "" else None
    query = db.query(PropertyDB)

    # Apply filters dynamically
    if area:
        query = query.filter(PropertyDB.location.ilike(f"%{area}%"))
    if purpose:
        query = query.filter(PropertyDB.purpose == purpose)
    if property_type:
        query = query.filter(PropertyDB.property_type == property_type)
    if min_price:
        query = query.filter(PropertyDB.final_price >= min_price)
    if max_price:
        query = query.filter(PropertyDB.final_price <= max_price)
    if bedrooms:
        query = query.filter(PropertyDB.bedrooms >= bedrooms)
    if bathrooms:
        query = query.filter(PropertyDB.bathrooms >= bathrooms)
    if min_sq_feet:
        query = query.filter(PropertyDB.area_sq_feet >= min_sq_feet)
    if max_sq_feet:
        query = query.filter(PropertyDB.area_sq_feet <= max_sq_feet)
    if min_sq_yards:
        query = query.filter(PropertyDB.area_sq_yards >= min_sq_yards)
    if max_sq_yards:
        query = query.filter(PropertyDB.area_sq_yards <= max_sq_yards)
    return query.limit(100).all()
   
@app.get("/get_all_areas")
async def get_all_areas(db: Session = Depends(get_db)):
    results = db.query(PropertyDB.location).distinct().all()
    areas = [row[0] for row in results if row[0]]
    areas.sort()
    return {"areas": areas}

# --- ADD ---

@app.post("/add_property")
def add_property(property_data: Property, db: Session = Depends(get_db)):
    new_property = PropertyDB(
        location=property_data.location,
        area_sq_feet=property_data.area_sq_feet,
        area_sq_yards=property_data.area_sq_yards,
        final_price=property_data.final_price,
        bedrooms=property_data.bedrooms,
        bathrooms=property_data.bathrooms,
        purpose=property_data.purpose,
        property_type=property_data.property_type
    )
   
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return {"message": "Property added successfully!"}

# --- UPDATE ---
@app.put("/update_property/{property_id}")
def update_property(property_id: int, updated_data: dict, db: Session = Depends(get_db)):
    # Query the DATABASE model (PropertyDB)
    prop = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
   
    # Update only provided fields
    for key, value in updated_data.items():
        if hasattr(prop, key):
            setattr(prop, key, value)
   
    db.commit()
    db.refresh(prop)
    return {"message": "Property updated!"}

# --- DELETE ---
@app.delete("/delete_property/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    # Query the DATABASE model (PropertyDB)
    prop = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
   
    db.delete(prop)
    db.commit()
    return {"message": "Property deleted!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5002)

from sqlalchemy import inspect
