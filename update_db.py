from MAIN import engine, Base
from MAIN import engine, Base, ActivityLog
# This command tells SQLAlchemy to check for missing tables
# and create them without touching existing data.
Base.metadata.create_all(bind=engine)
print("Database updated successfully!")