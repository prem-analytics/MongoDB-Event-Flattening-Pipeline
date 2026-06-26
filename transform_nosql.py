import duckdb

def flatten_unstructured_events():
    print("🧠 Spinning up SQL Flattening Engine inside DuckDB...")
    
    # Connect to our local database warehouse file
    db_conn = duckdb.connect("unstructured_analytics.db")
    
    print("⚡ Unnesting arrays and parsing JSON objects to relational rows...")
    
    # This SQL query rips open the inner structures dynamically
    db_conn.execute("""
        CREATE OR REPLACE TABLE fct_flattened_order_items AS 
        WITH unboxed_items AS (
            SELECT 
                event_id,
                user_id,
                -- Cast the timestamp safely to a standard DATETIME format
                CAST(timestamp AS TIMESTAMP) as event_timestamp,
                
                -- Extract simple nested objects from the metadata column using dot notation
                metadata.device AS user_device,
                metadata.ip AS user_ip_address,
                
                -- UNNEST blows up the list of items into separate rows!
                UNNEST(cart_items) as raw_item
            FROM stg_raw_mongodb_logs
        )
        SELECT 
            event_id,
            user_id,
            event_timestamp,
            user_device,
            user_ip_address,
            
            -- Extract individual keys out of the newly isolated item objects
            raw_item.item_name AS item_name,
            raw_item.category AS item_category,
            CAST(raw_item.price AS DOUBLE) AS item_price,
            CAST(raw_item.quantity AS INT) AS item_quantity,
            
            -- Compute derived analytical columns on the fly
            round(CAST(raw_item.price AS DOUBLE) * CAST(raw_item.quantity AS INT), 2) as total_item_revenue
            
        FROM unboxed_items;
    """)
    
    # Verify our engineering work by printing the new flat table schema and rows
    check_df = db_conn.execute("""
        SELECT 
            event_id, 
            user_device, 
            item_name, 
            item_quantity, 
            total_item_revenue 
        FROM fct_flattened_order_items
    """).df()
    
    print("\n✅ Relational Model Transformation Complete! Previewing Flattened Data Warehouse Rows:")
    print(check_df)
    
    db_conn.close()

if __name__ == "__main__":
    flatten_unstructured_events()