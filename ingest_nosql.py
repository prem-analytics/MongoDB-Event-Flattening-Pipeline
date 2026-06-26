import mongomock
import duckdb
import pandas as pd

def generate_mock_mongodb_data():
    print("🔌 Initializing Mock MongoDB Client Store...")
    # Create a virtual, in-memory NoSQL database instance
    client = mongomock.MongoClient()
    db = client.ecommerce_warehouse
    events_collection = db.user_event_logs
    
    # Deeply nested unstructured JSON documents (simulate raw app events)
    mock_logs = [
        {
            "event_id": "ev_101",
            "user_id": "usr_99",
            "timestamp": "2026-06-25T10:00:00Z",
            "metadata": {"device": "Mobile", "ip": "192.168.1.5"},
            "cart_items": [
                {"item_name": "Mechanical Keyboard", "category": "Tech", "price": 120.00, "quantity": 1},
                {"item_name": "Ergonomic Mouse", "category": "Tech", "price": 80.00, "quantity": 2}
            ]
        },
        {
            "event_id": "ev_102",
            "user_id": "usr_44",
            "timestamp": "2026-06-25T11:15:00Z",
            "metadata": {"device": "Desktop", "ip": "203.0.113.42"},
            "cart_items": [
                {"item_name": "4K Gaming Monitor", "category": "Tech", "price": 450.00, "quantity": 1}
            ]
        },
        {
            "event_id": "ev_103",
            "user_id": "usr_99",
            "timestamp": "2026-06-25T14:30:00Z",
            "metadata": {"device": "Mobile", "ip": "192.168.1.5"},
            "cart_items": [
                {"item_name": "Protein Shaker", "category": "Fitness", "price": 25.00, "quantity": 1},
                {"item_name": "Resistance Bands", "category": "Fitness", "price": 15.00, "quantity": 3},
                {"item_name": "Yoga Mat", "category": "Fitness", "price": 40.00, "quantity": 1}
            ]
        }
    ]
    
    # Insert JSON data logs directly into our mock NoSQL collection
    events_collection.insert_many(mock_logs)
    print(f"📥 Successfully seeded {events_collection.count_documents({})} nested raw logs into MongoDB.")
    
    # --- EXTRACTION LAYER ---
    print("🛰️ Streaming and extracting unstructured collections from NoSQL...")
    raw_cursor = events_collection.find({}, {"_id": 0}) # Ignore the default MongoDB ObjectIDs
    raw_documents = list(raw_cursor)
    
    # Convert list of Python dictionaries to a pandas DataFrame containing raw JSON objects
    df_raw = pd.DataFrame(raw_documents)
    
    # Dump the raw unparsed JSON directly into DuckDB as our Raw Landed Staging layer
    db_conn = duckdb.connect("unstructured_analytics.db")
    db_conn.execute("CREATE OR REPLACE TABLE stg_raw_mongodb_logs AS SELECT * FROM df_raw")
    
    print("💾 Raw JSON documents landed successfully into DuckDB staging storage!")
    db_conn.close()

if __name__ == "__main__":
    generate_mock_mongodb_data()