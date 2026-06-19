# ZameenAI: Karachi Real Estate Portal & ML Valuation Engine

A collaborative full-stack real estate platform that structures raw Pakistani housing datasets, tracks regional listings via an integrated relational SQLite database, provides administrative data control, and runs automated machine learning regressions to forecast property valuations instantly.

---

## 👥 Team & Contributions

This project was built as a coordinated full-stack engineering effort:

* **[Muhammad Rayan](https://github.com/rayisdbest)** — *Data Science, Machine Learning, & Database Engineering*
    * **Data Pipeline Pipeline:** Isolated raw national data records to construct clean, dedicated sub-frames for Karachi properties and sub-unit portions. Corrected missing/erroneous value blocks (0-bedroom/0-bathroom rows), removed unnecessary data, and implemented automated inflation scaling metrics.
    * **Machine Learning:** Engineered pre-processing scaling steps and trained a high-accuracy `HistGradientBoostingRegressor` to handle mixed categorical and numerical data. 
    * **Database Architecture:** Built structural SQL data tables using Python's relational `sqlite3` driver to initialize local persistent ledger tracking.

* **[Zainab](https://github.com/zainbhumd)** — *Backend Engineering & Web Integration*
    * **Backend REST API:** Engineered an operational server application utilizing the **FastAPI** framework to manage live HTTP client request handling.
    * **Database Synchronization:** Structured SQLAlchemy Object-Relational Mapping (ORM) and Pydantic schema validation wrappers to execute secure listing queries, updates, and deletion pipelines.
    * **Web Portal Interface:** Developed the functional web application interface core (`index.html`), managing structural state integration to link browser interaction hooks to live server ports.

---

## 🚀 Key Features

* **AI Price Predictor:** Generates optimized market price forecasts based on real-time user selections (location, size dimensions, rooms, type) through the saved machine learning pipeline.
* **Single-Page Tabbed Architecture:** Features a fluid UI dashboard built using Tailwind CSS that transitions between application modules instantly without screen-flickering or full-page browser reloads.
* **Database Filtration Engine:** Executes advanced SQL relational queries, letting users parse records using multiple criteria like area locations, min/max price boundaries, and unit types.
* **Administrative CRUD Operations:** Provides front-end form controls to securely create new property listings, update active pricing variables, or delete records directly from the database.

---

## ⚠️ Data Limitations & Future Scope
* **Data Volume Constraint:** While the predictive engine is optimized using a `HistGradientBoostingRegressor`, real-world property markets fluctuate rapidly. Because national real estate data can be limited or sparse in specific sub-localities, certain niche property predictions may exhibit variance. 
* **Next Steps:** Future iterations of this project will involve setting up web-scrapers to continuously feed live data into the pipeline to improve model accuracy across all sectors of Karachi.
---

## 🛠️ Tech Stack

* **Data Science / Machine Learning:** Python, Pandas, Scikit-Learn (HistGradientBoostingRegressor), Joblib, Pickle
* **Backend Framework:** FastAPI, Uvicorn ASGI Server, SQLAlchemy ORM, Pydantic
* **Database Storage:** SQLite3 Relational Engine
* **Frontend Web Layout:** HTML5, JavaScript (Fetch API Engine), Tailwind CSS (Utility Framework)

---

## 📂 Project Architecture

```text
📁 python-projects/              # Main Git Root Directory
│
├── 📁 data/                     # Structured Dataset Storage
│   ├── Karachi property.csv
│   └── Upper and Lower portions.csv
│
├── 📁 models/                   # Saved ML Weight Files
│   ├── column_transformer.pkl
│   ├── main_property_model.pkl
│   └── portions_model.pkl
│
├── 📁 templates/                # Web Application View Shells
│   └── index.html               # Main Single-Page UI File
│
├── 📜 karachi_housing.db        # Live Local SQLite Relational Database File
├── 📜 MAIN.py                   # Operational FastAPI Backend Application Code
├── 📜 data_pipeline.py          # CSV Data Preparation & Scaling Script
├── 📜 train_models.py           # Model Training & Pipeline Serialization Script
├── 📜 build_database.py         # Relational DB Engine Migration Script
└── 📜 README.md                 # Project Overview Documentation
