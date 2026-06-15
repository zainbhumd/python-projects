from datetime import datetime
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# what an incoming property has to look like
class Property(BaseModel):
    area: str
    price: float
    bedrooms: int
    size: float
    unit: str
    type: str

# testing data
karachi_properties = [
    {"id": 1, "area": "DHA Phase 6", "price": 35000000, "bedrooms": 3, "size": 500, "unit": "sq yds", "type": "house"},
    {"id": 2, "area": "Clifton", "price": 22000000, "bedrooms": 3, "size": 1800, "unit": "sq ft", "type": "apartment"},
    {"id": 3, "area": "DHA City", "price": 8500000, "bedrooms": 0, "size": 125, "unit": "sq yds", "type": "plot"}
]

# 1 Search filter
@app.get("/search")
def search_properties(
    area: Optional[str] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    min_size: Optional[float] = None,
    unit: Optional[str] = None,
    property_type: Optional[str] = None
):
    results = []
    
    for prop in karachi_properties:
        match = True
        
        if area and area.lower() not in prop["area"].lower():
            match = False
            
        if max_price:
            try:
                prop_price = float(prop["price"])
                if prop_price > max_price:
                    match = False
            except (ValueError, TypeError):
                match = False
                
        if bedrooms and prop.get("bedrooms") != bedrooms:
            match = False
            
        if unit and unit.lower() != prop.get("unit", "").lower():
            match = False
            
        if min_size and prop.get("size", 0) < min_size:
            match = False
            
        if property_type and property_type.lower() != prop.get("type", "").lower():
            match = False
            
        if match:
            results.append(prop)
            
    return {"results": results}

# 2 Add a new property
@app.post("/add-property")
def add_new_property(new_prop: Property):
    next_id = max([p["id"] for p in karachi_properties]) + 1 if karachi_properties else 1
    property_dict = new_prop.model_dump()
    property_dict["id"] = next_id
    karachi_properties.append(property_dict)
    with open("activity_log.txt", "a") as log: log.write(f"[{datetime.now()}] ADDED: Property ID {next_id} in {property_dict['area']}\n")
    return {"message": "Property added successfully!", "added_property": property_dict}

# 3 Update an existing property
@app.put("/update-property/{property_id}")
def update_property(property_id: int, updated_fields: Property):
    for prop in karachi_properties:
        if prop["id"] == property_id:
            prop["area"] = updated_fields.area
            prop["price"] = updated_fields.price
            prop["bedrooms"] = updated_fields.bedrooms
            prop["size"] = updated_fields.size
            prop["unit"] = updated_fields.unit
            prop["type"] = updated_fields.type
            with open("activity_log.txt", "a") as log: log.write(f"[{datetime.now()}] UPDATED: Property ID {property_id} price changed to {updated_fields.price}\n")
            return {"message": f"Property {property_id} updated successfully!", "updated_property": prop}
            
    return {"error": f"Property with ID {property_id} not found."}
# 4 Delete a property
@app.delete("/delete-property/{property_id}")
def delete_property(property_id: int):
    for prop in karachi_properties:
        if prop["id"] == property_id:
            karachi_properties.remove(prop)
            with open("activity_log.txt", "a") as log: log.write(f"[{datetime.now()}] DELETED: Property ID {property_id}\n")
            return {"message": f"Property {property_id} has been removed successfully!"}
            
    return {"error": f"Property with ID {property_id} not found."}