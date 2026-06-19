import pandas as pd

# =====================================================================
# STEP 1: LOAD DATA & FILTER BY CITY
# =====================================================================
df = pd.read_csv(r"C:\Users\Pc\OneDrive\Work\pakistan property.csv")

# FIX: Ensure we are only dealing with Karachi properties moving forward
df = df[df['city'] == 'Karachi'].copy()


# =====================================================================
# STEP 2: DEFINE TEXT PROCESSING CONVERSION FUNCTIONS
# =====================================================================
def convert_to_sq_feet(area_text):
    try:
        area_text = str(area_text).lower().strip()
        number = float(area_text.split()[0]) 
        if 'marla' in area_text: return number * 225
        elif 'kanal' in area_text: return number * 4500
        return None
    except: return None

def convert_to_sq_yards(area_text):
    try:
        area_text = str(area_text).lower().strip()
        number = float(area_text.split()[0])
        if 'marla' in area_text: return number * 25
        elif 'kanal' in area_text: return number * 500
        return None
    except: return None


# =====================================================================
# STEP 3: TEXT PARSING & COLUMN CLEANUP
# =====================================================================
df['area_sq_feet'] = df['area'].apply(convert_to_sq_feet)
df['area_sq_yards'] = df['area'].apply(convert_to_sq_yards)

# Drop missing values resulting from unparsable text formats
df = df.dropna(subset=['area_sq_feet', 'area_sq_yards'])

# Permanently drop old unneeded structural tracking features
df.drop(columns=['area', 'location_id', 'province_name', 'latitude', 'longitude', 'date_added', 'agency', 'agent', 'page_url'], inplace=True, errors='ignore')

# Standardize feature records
df['property_type'] = df['property_type'].replace('Penthouse', 'Flat')


# =====================================================================
# STEP 4: DATA CLEANUP (DROP LOGICAL ANOMALIES)
# =====================================================================
# FIX: Permanently remove properties containing 0 bedrooms or 0 bathrooms
zero_mask = (df['bedrooms'] == 0) | (df['baths'] == 0)
df = df.loc[~zero_mask].copy()

# Rename the column 'baths' to 'bathrooms' permanently
df.rename(columns={'baths': 'bathrooms'}, inplace=True)
# =====================================================================
# STEP 5: FINANCIAL DATA TRANSFORMATION (INFLATION MATH)
# =====================================================================
df['final_price'] = df['price'].copy().astype(float)

# Inflation index tracking schema for 2026 value updates
# format: { 'Area Context Name': (Sale Multiplier, Rent Multiplier) }
inflation_index = {
    'DHA Defence': (4.2, 3.0),
    'Clifton': (4.5, 3.4),
    'Bath Island': (4.5, 3.4),
    'Gizri': (4.5, 3.4),
    'Bahria Town Karachi': (3.4, 2.8),
    'Scheme 33': (3.8, 3.1),
    'Gulshan-e-Iqbal Town': (3.7, 3.0),
    'Nazimabad': (3.5, 2.9),
    'North Nazimabad': (3.5, 2.9),
    'Malir': (3.3, 2.7),
    'Cantt': (3.3, 2.7),
    'Falcon Complex Faisal': (3.3, 2.7),
    'Federal B Area': (3.3, 2.6),
    'Shahra-e-Faisal': (3.3, 2.6),
    'Gulistan-e-Jauhar': (3.6, 2.9),
    'Jamshed Town': (3.3, 2.6),
    'Korangi': (3.3, 2.6),
    'Landhi': (3.3, 2.6),
    'Shah Faisal Town': (3.3, 2.6)
}

# Apply area-specific mapping updates
for area, multipliers in inflation_index.items():
    sale_multi = multipliers[0]
    rent_multi = multipliers[1]
    
    filt_s = (df['location'] == area) & (df['purpose'] == 'For Sale')
    df.loc[filt_s, 'final_price'] = df.loc[filt_s, 'final_price'] * sale_multi 	
    
    filt_r = (df['location'] == area) & (df['purpose'] == 'For Rent')
    df.loc[filt_r, 'final_price'] = df.loc[filt_r, 'final_price'] * rent_multi   

# Apply general default multipliers to all outlier regions left out of the dictionary
completed_areas = list(inflation_index.keys())

filt_default_sale = (~df['location'].isin(completed_areas)) & (df['purpose'] == 'For Sale') 
df.loc[filt_default_sale, 'final_price'] = df.loc[filt_default_sale, 'final_price'] * 3.2

filt_default_rent = (~df['location'].isin(completed_areas)) & (df['purpose'] == 'For Rent')
df.loc[filt_default_rent, 'final_price'] = df.loc[filt_default_rent, 'final_price'] * 2.6

# Scale structural discount values specific to portions
Portions_sale = ((df['property_type'] == 'Upper Portion') | (df['property_type'] == 'Lower Portion')) & (df['purpose'] == 'For Sale')
df.loc[Portions_sale, 'final_price'] = df.loc[Portions_sale, 'final_price'] * 0.8


# =====================================================================
# STEP 6: EXPORT TO TARGET DATASETS
# =====================================================================
main_properties = df['property_type'].isin(['House', 'Flat'])
portions = ~main_properties

# Divide files cleanly into context-specific subsets
main_properties_df = df[main_properties]
portions_df = df[portions]

# Save outputs to disk
main_properties_df.to_csv(r"C:\Users\Pc\OneDrive\Work\Karachi property_test.csv", index=False)
portions_df.to_csv(r"C:\Users\Pc\OneDrive\Work\Upper and Lower portions_test.csv", index=False)
