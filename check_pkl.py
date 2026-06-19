import joblib

# Load the transformer
transformer = joblib.load("models/column_transformer.pkl")

# 1. Print the expected input features (column names)
print("Expected Input Columns:")
print(transformer.feature_names_in_)

# 2. Print the categories for each categorical column
print("\nCategorical Categories (Location, Purpose, etc.):")
for name, transformer_step in transformer.named_transformers_.items():
    # This assumes a standard pipeline with a OneHotEncoder
    if hasattr(transformer_step, 'categories_'):
        print(f"Column '{name}' has categories: {transformer_step.categories_}")