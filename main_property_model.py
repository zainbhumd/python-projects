import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingRegressor
import pickle

# Step 1
df = pd.read_csv(r"C:\Users\Pc\OneDrive\Work\Karachi property.csv")
X = df[['location', 'bathrooms', 'bedrooms', 'purpose', 'property_type', 'area_sq_yards']]
y = df['final_price']
# Step 2
ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
ct = make_column_transformer(
    (ohe , ['location', 'property_type', 'purpose']),
    remainder ='passthrough'
    )
ct.set_output(transform='pandas')
X_processed = ct.fit_transform(X)
# Step 3
X_train, X_test, y_train, y_test = train_test_split(X_processed , y, test_size = 0.2, random_state= 42)
# Step 4
model = HistGradientBoostingRegressor(
    loss ='absolute_error',
    learning_rate = 0.03,
    max_iter = 300,
    max_leaf_nodes = 50,
    min_samples_leaf = 15
    )

model.fit(X_train, y_train)

accuracy_score = model.score(X_test, y_test)
print(f'Accuracy score: {accuracy_score * 100:.2f}%')

with open('main_property_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('column_transformer.pkl', 'wb') as f:
    pickle.dump(ct, f)