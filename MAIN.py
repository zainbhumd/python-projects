from fastapi import FastAPI

app = FastAPI()

karachi_properties = [
    {"id": 1, "area": "DHA Phase 6", "price": 35000000, "bedrooms": 3, "size": 500, "unit": "sq yds", "type": "house"},
    {"id": 2, "area": "Clifton", "price": 22000000, "bedrooms": 3, "size": 1800, "unit": "sq ft", "type": "apartment"},
    {"id": 3, "area": "DHA City", "price": 12000000, "bedrooms": 0, "size": 125, "unit": "sq yds", "type": "plot"}
]
# 1. Fetch all properties
@app.get("/")
def get_all_properties():
    return {"properties": karachi_properties}

# 2. Add a new property
@app.post("/add-property")
def add_new_property(new_property: dict):
    karachi_properties.append(new_property)
    return {"message": "Property added successfully!", "added": new_property}

# 3. Status check endpoint
@app.get("/status")
def system_status():
    return {"status": "Online", "database": "Connected"}
@app.get("/search")
def search_properties(
    area: str = None, 
    max_price: float = None, 
    bedrooms: int = None, 
    min_size: float = None, 
    unit: str = None,
    property_type: str = None
):
    results = []
    
    for prop in karachi_properties:
        match = True
        
        # 1. Filter by Area
        if area and area.lower() not in prop["area"].lower():
            match = False
            
        # 2. Filter by Maximum Price
        if max_price:
            try:
                prop_price = float(prop["price"])
                if prop_price > max_price:
                    match = False
            except (ValueError, TypeError):
                match = False
                
        # 3. Filter by Exact Bedrooms
        if bedrooms and prop.get("bedrooms") != bedrooms:
            match = False
            
        # 4. Filter by Unit Type
        if unit and unit.lower() != prop.get("unit", "").lower():
            match = False
            
        # 5. Filter by Minimum Size
        if min_size and prop.get("size", 0) < min_size:
            match = False
            
        # 6. Filter by Property Type
        if property_type and property_type.lower() != prop.get("type", "").lower():
            match = False
            
        if match:
            results.append(prop)
            
    return {"results": results}