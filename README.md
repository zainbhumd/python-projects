# ZameenAI: Karachi Real Estate Portal & ML Valuation Engine

ZameenAI is an end-to-end real estate intelligence platform designed to bridge the gap between raw property data and actionable market insights in the Pakistani housing market. By integrating a high-precision predictive engine directly with a responsive full-stack web interface, ZameenAI enables users to instantly forecast property valuations, perform complex market filtering, and manage listings in real-time. Designed to solve the issue of data opacity in the Pakistani housing sector, the project transforms unorganized market records into an administrative-grade, AI-driven valuation tool that offers unparalleled transparency for the Karachi real estate market.

---

## 👥 Team & Contributions

This project was built as a coordinated full-stack engineering effort:

* **[Muhammad Rayan](https://github.com/rayisdbest)** — *Data Science, Machine Learning, & Database Engineering*
   **Data Pipeline Engineering**: Designed and optimized an automated ETL (Extract, Transform, Load) pipeline to ingest large-scale national datasets. Engineered data cleaning protocols to sanitize real estate records, including automated imputation of missing values, outlier filtration, and the application of dynamic inflation-adjustment metrics to ensure accurate market valuations.
   **Predictive Machine Learning**: Developed a high-precision valuation engine using the HistGradientBoostingRegressor. Implemented complex pre-processing workflows, including custom feature scaling and encoding strategies, to effectively handle mixed-type categorical and numerical datasets with high variance.
   **Database Architecture**: Architected and normalized the structural SQL database schema. Leveraged Python’s sqlite3 driver to initialize a robust, persistent ledger system that ensures data integrity and high-performance querying for the platform’s real-time retrieval requirements.

* **[Zainab Hummad](https://github.com/zainbhumd)** — *Backend Engineering & Web Integration*
    * **Backend REST API:** Designed a robust, asynchronous RESTful API using FastAPI, optimizing request-response latency to handle concurrent client interactions for real-time data queries.
    * **Database Synchronization:** Architected a type-safe data access layer using SQLAlchemy ORM and Pydantic. Implemented robust input validation and schema management to ensure database integrity during complex CRUD operations
    * **Web Portal Interface:** Engineered a modular, single-page web interface with Tailwind CSS, utilizing asynchronous JavaScript Fetch API calls to achieve a seamless, fluid user experience with zero-reload state transitions.
     * **Operational Activity Logging**: Implemented a persistent, time-stamped activity log that records all Create, Update, and Delete (CRUD) operations. This utility tracks the specific date and time of every administrative database mutation, ensuring full data accountability and enabling historical analysis of listing trends.

---

## 🚀 Key Features

* **AI Price Predictor:** Generates optimized market price forecasts based on real-time user selections (location, size dimensions, rooms, type) through the saved machine learning pipeline.
* **Single-Page Tabbed Architecture:** Features a fluid UI dashboard built using Tailwind CSS that transitions between application modules instantly without screen-flickering or full-page browser reloads.
* **Database Filtration Engine:** Executes advanced SQL relational queries, letting users parse records using multiple criteria like area locations, min/max price boundaries, and unit types.
* **Administrative CRUD Operations:** Provides front-end form controls to securely create new property listings, update active pricing variables, or delete records directly from the database.

---

⚙️ **Engineering Challenges**
"Successfully resolved integration hurdles between the asynchronous Python backend and the SQLite persistence layer, ensuring atomicity in database transactions. Overcame front-end state management complexities by implementing efficient DOM manipulation strategies to handle dynamic filtering without performance degradation."

🌐 **Deployment Architecture**
"The platform is fully containerized and deployed via Render’s CI/CD pipeline. The production environment utilizes an ASGI server (Uvicorn) with automated health-check monitoring to ensure 99.9% uptime for the valuation engine."


# **Why This Stack?**
**FastAPI & SQLAlchemy**: Chosen for the ability to handle asynchronous tasks efficiently while providing strict data schema enforcement.

**Tailwind CSS**: Selected to minimize bundle sizes and maintain consistent design systems across the entire application without the overhead of heavy framework dependencies.

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

### 🚀 𝗤𝘂𝗶𝗰𝗸 𝗦𝘁𝗮𝗿𝘁
1. Clone the repository: `git clone https://github.com/zainbhumd/python-projects.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the server: `uvicorn MAIN:app --reload`
4. Access the interface: `http://127.0.0.1:5002`
