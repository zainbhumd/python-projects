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
import joblib
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from fastapi.responses import FileResponse
import pandas as pd
from sqlalchemy import func


# 1. Setup
app = FastAPI()
Base = declarative_base()
# Use relative path for Render/GitHub compatibility
import os
db_path = os.path.join(os.path.dirname(__file__), "karachi_housing.db")
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

from fastapi import FastAPI, Depends, HTTPException

# 2. Load Models
# Ensure these files exist in a /models folder in your repo
transformer = joblib.load("models/column_transformer.pkl")
main_model = joblib.load("models/main_property_model.pkl")


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

# 3. Database Model
class PropertyDB(Base):
    __tablename__ = "main_properties"
    property_id = Column(Integer, primary_key=True)
    property_type = Column(String)
    final_price = Column(Float)
    location = Column(String)
    bathrooms = Column(Integer)
    bedrooms = Column(Integer)
    purpose = Column(String)
    area_sq_feet = Column(Float)
    area_sq_yards = Column(Float)

Base.metadata.create_all(bind=engine)

# 4. Schemas
class PropertySchema(BaseModel):
    property_id: int
    property_type: str
    location: str
    bathrooms: int
    bedrooms: int
    purpose: str
    area_sq_feet: float
    area_sq_yards: float
    final_price: float

class AIInput(BaseModel):
    location: str
    property_type: str
    purpose: str
    bathrooms: str
    bedrooms: str
    area_sq_yards: str

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)  # "Added", "Updated", or "Deleted"
    property_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
def log_activity(db, action, property_id):
    log = ActivityLog(action=action, property_id=property_id)
    db.add(log)
    db.commit()
    
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.get("/get_logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(ActivityLog).all()

# 5. Endpoints
@app.get("/")
async def home(): return FileResponse("templates/index.html")

@app.post("/predict_price")
def predict_price(data: AIInput):
    # Convert empty strings or None to 0, otherwise convert to int
    def to_int(val):
        return int(val) if val and str(val).strip() != "" else 0

    input_dict = {
        'location': data.location,
        'property_type': data.property_type,
        'bathrooms': to_int(data.bathrooms),
        'bedrooms': to_int(data.bedrooms),
        'purpose': data.purpose,
        'area_sq_yards': float(data.area_sq_yards) if data.area_sq_yards else 0.0
    }
    
    # Create DataFrame and predict
    input_df = pd.DataFrame([input_dict])
    processed_data = transformer.transform(input_df)
    prediction = main_model.predict(processed_data)
    
    return {"predicted_price": float(prediction[0])}

from fastapi import Depends

from sqlalchemy.orm import Session

@app.get("/properties")
def get_properties(
    db: Session = Depends(get_db),
    area: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    purpose: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    min_sq: Optional[float] = None,
    max_sq: Optional[float] = None,
    unit: str = "sq_yards"
):
    query = db.query(PropertyDB)

    is_blank = not any([area, min_price, max_price, property_type, purpose])

    if is_blank:
        # Fetch 100 random properties
        results = query.order_by(func.random()).limit(100).all()
    else:

        if area:
            print(f"DEBUG: Filtering by location containing: {area}")
            query = query.filter(PropertyDB.location.ilike(f"%{area}%"))
        if property_type:
            query = query.filter(PropertyDB.property_type == property_type)
        if min_price:
            print(f"DEBUG: Filtering properties with price >= {min_price}")
            count = query.filter(PropertyDB.final_price >= min_price).count()
            print(f"DEBUG: {count} properties match the price criteria")
            query = query.filter(PropertyDB.final_price >= min_price)
        if max_price:
            print(f"DEBUG: Filtering properties with price <= {max_price}")
            count = query.filter(PropertyDB.final_price <= max_price).count()
            print(f"DEBUG: {count} properties match the max price criteria")
            query = query.filter(PropertyDB.final_price <= max_price)
        if purpose and purpose != "Any":
            # Create a mapping to bridge the gap between UI labels and DB values
            purpose_map = {
                "Sale": "For Sale",
                "Rent": "For Rent"
            }
            # Get the database-specific string, or default to the original input
            db_purpose = purpose_map.get(purpose, purpose)
            
            print(f"DEBUG: Filtering by purpose: '{purpose}' mapped to '{db_purpose}'")
            
            # Use ilike for a case-insensitive, flexible match
            query = query.filter(PropertyDB.purpose.ilike(f"%{db_purpose}%"))
            
            # Keep your debug count check
            count = query.count()
            print(f"DEBUG: {count} properties match the purpose criteria")
        if bedrooms:
            query = query.filter(PropertyDB.bedrooms >= bedrooms)
        if bathrooms:
            query = query.filter(PropertyDB.bathrooms >= bathrooms)
        if unit == "sq_yards":
            if min_sq:
                query = query.filter(PropertyDB.area_sq_yards >= min_sq)
            if max_sq:
                query = query.filter(PropertyDB.area_sq_yards <= max_sq)
        else:
            if min_sq:
                query = query.filter(PropertyDB.area_sq_feet >= min_sq)
            if max_sq:
                query = query.filter(PropertyDB.area_sq_feet <= max_sq)

        results = query.all()
    print(f"DEBUG: Query returned {len(results)} properties")
    return results

@app.post("/add_property")
def add_property(p: PropertySchema, db: Session = Depends(get_db)):
    # Create the DB entry using the validated Pydantic model data
    new_prop = PropertyDB(
        property_id=p.property_id,
        location=p.location,
        property_type=p.property_type,
        final_price=p.final_price,
        purpose=p.purpose,
        bedrooms=p.bedrooms,
        bathrooms=p.bathrooms,
        area_sq_yards=p.area_sq_yards,
        area_sq_feet=p.area_sq_feet
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    log_activity(db, "Added", new_prop.property_id)
    return {"message": "Property added successfully!"}

@app.put("/update_property/{property_id}")
def update_property(property_id: int, data: dict, db: Session = Depends(get_db)):
    # 1. Locate the record
    prop = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # 2. Specifically update only the price
    if "final_price" in data:
        prop.final_price = float(data["final_price"])
    else:
        raise HTTPException(status_code=400, detail="Price is required for update")
    
    db.commit()
    db.refresh(prop)
    log_activity(db, "Updated", prop.property_id)
    return {"message": f"Price for Property {property_id} updated successfully!"}

@app.delete("/delete_property/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    # 1. Locate the record
    prop = db.query(PropertyDB).filter(PropertyDB.property_id == property_id).first()
    
    # 2. Check if it exists
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    # 3. Remove it
    db.delete(prop)
    db.commit()
    log_activity(db, "Deleted", prop.property_id)
    return {"message": "Property deleted successfully!"}