# Web Scraping & ETL Projects with Python

This repository contains two Python-based data projects demonstrating **web scraping**, **data transformation**, and **ETL (Extract, Transform, Load)** processes. The scripts cover both static and dynamic data sources, and include data cleaning, storage, and logging mechanisms.

---

## 📁 Project 1 – `glob/`  
**ETL Pipeline: CSV, JSON & XML Data Consolidation**

### 🔍 Description
This project extracts structured data (name, height, weight) from multiple formats: `.csv`, `.json`, and `.xml`. It performs unit conversions (inches to meters, pounds to kilograms), logs each phase of the ETL process, and saves the transformed data to a CSV file.

### 🛠 Technologies
- `pandas`
- `glob`
- `xml.etree.ElementTree`
- `datetime`

### 📌 Features
- Reads data from all CSV, JSON, and XML files in the `data/` folder.
- Transforms height and weight units.
- Logs every step in `log_file.txt`.
- Exports the cleaned data to `data/transformed_data.csv`.

### ▶️ How to Run
```bash
cd glob
python etl_script.py
```

---

## 📁 Project 2 – `gdp/`  
**Web Scraping & ETL: Countries by GDP (Wikipedia)**

### 🔍 Description
This project scrapes GDP data from a snapshot of the Wikipedia page _List of countries by GDP (nominal)_, transforms the values from millions to billions, and stores the final output into a `.csv` file and an SQLite database.

### 🛠 Technologies
- `pandas`, `numpy`
- `BeautifulSoup` (`bs4`)
- `requests`
- `sqlite3`
- `datetime`

### 📌 Features
- Extracts country names and GDP values from an HTML table.
- Cleans and converts currency data to numeric format.
- Loads results into both CSV and SQLite formats.
- Logs each step of the pipeline in `data/etl_project_log.txt`.

### ▶️ How to Run
```bash
cd gdp
python etl_script.py
```

---

## ✅ Author
Ahmadou Barry  
📧 barryahmadou135@gmail.com  

---

## 📁 Repository Structure
```
.
├── glob/               # ETL from local CSV, JSON, XML files
│   └── etl_code.py
│
├── gdp/                # Web scraping + ETL from Wikipedia (archived)
│   └── etl_project_gdp.py
│
└── README.md           # This file
```

---

## 🗃 Sample Outputs
- CSV files with cleaned and standardized data
- SQL database table (`World_Economies.db`)
- Execution logs for debugging and traceability
