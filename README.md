# 🛰️ MongoDB Event Flattening Pipeline

An end-to-end data analytics pipeline that ingests semi-structured NoSQL JSON event logs from MongoDB, streams them into an embedded DuckDB data warehouse layer, and utilizes advanced SQL transformation modeling to flatten nested document arrays into analytical data marts.

🔗 **[Click Here to View the Live Interactive Dashboard](https://prem-analytics-mongodb-event-flattening-pipeline-app-n4cwmz.streamlit.app/)**

---

## 📊 Live Dashboard Preview
<video src="dashboard_preview1.mp4" width="100%" autoplay loop muted controls></video>

---

## 🛠️ Tech Stack & Architecture
* **Source Layer (NoSQL Store):** MongoDB simulation (`mongomock` / `pymongo`)
* **Data Warehouse Storage:** DuckDB (Columnar analytical warehouse)
* **Transformation Modeling:** Advanced Embedded SQL (`UNNEST()`, dot-notation parsing)
* **Visualization Layer:** Streamlit Cloud Network Interface