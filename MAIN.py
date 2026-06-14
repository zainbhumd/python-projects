from fastapi import FastAPI

app = FastAPI()

karachi_properties = [
    {
        "id": 1, 
        "area": "DHA Phase 6", 
        "type": "Apartment", 
        "price": "3.5 Crore", 
        "bedrooms": 3
    },
    {
        "id": 2, 
        "area": "Gulshan-e-Iqbal", 
        "type": "House", 
        "price": "5.2 Crore", 
        "bedrooms": 4
    }
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